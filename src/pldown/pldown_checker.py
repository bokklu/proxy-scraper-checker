import asyncio
import logging
from aiohttp import ClientSession
from contracts.enums import ProxyType, Provider
from pldown.pldown_scraper import PldownScraper
from repositories.proxy_repo import ProxyRepo
from repositories.sql_repo import SqlRepo
from repositories.geo_repo import GeoRepo
from dataclasses import dataclass
from utils.task_pool import TaskPool
from utils.proxy_helper import ProxyHelper

@dataclass
class PldownChecker:
    _geo_repo: GeoRepo = GeoRepo(get_country=False)
    _pldown_scraper: PldownScraper = PldownScraper()
    _proxy_repo: ProxyRepo = ProxyRepo(get_access_type=False)
    _sql_repo: SqlRepo = SqlRepo()

    async def check_proxies(self):
        async with ClientSession() as client_session:
            pldown_http_task = asyncio.create_task(self._pldown_scraper.scrape(client_session, ProxyType.HTTP))
            pldown_https_task = asyncio.create_task(self._pldown_scraper.scrape(client_session, ProxyType.HTTPS))
            pldown_socks4_task = asyncio.create_task(self._pldown_scraper.scrape(client_session, ProxyType.SOCKS4))
            pldown_socks5_task = asyncio.create_task(self._pldown_scraper.scrape(client_session, ProxyType.SOCKS5))
            provider_proxies = await asyncio.gather(*[pldown_http_task, pldown_https_task, pldown_socks4_task, pldown_socks5_task])

        http_https_scrape_info = provider_proxies[0].intersection(provider_proxies[1])
        http_scrape_info = provider_proxies[0] - provider_proxies[1]
        https_scrape_info = provider_proxies[1] - provider_proxies[0]
        socks4_socks5_scrape_info = provider_proxies[2].intersection(provider_proxies[3])
        socks4_scrape_info = provider_proxies[2] - provider_proxies[3]
        socks5_scrape_info = provider_proxies[3] - provider_proxies[2]

        async with TaskPool(2000) as tasks:
            for scrape_info in http_https_scrape_info: await tasks.put(self._proxy_repo.ping_multiple_http(scrape_info))
            for scrape_info in http_scrape_info: await tasks.put(self._proxy_repo.ping_http(ProxyType.HTTP, scrape_info))
            for scrape_info in https_scrape_info: await tasks.put(self._proxy_repo.ping_http(ProxyType.HTTPS, scrape_info))
            for scrape_info in socks4_socks5_scrape_info: await tasks.put(self._proxy_repo.ping_multiple_socks(scrape_info))
            for scrape_info in socks4_scrape_info: await tasks.put(self._proxy_repo.ping_socks(ProxyType.SOCKS4, scrape_info))
            for scrape_info in socks5_scrape_info: await tasks.put(self._proxy_repo.ping_socks(ProxyType.SOCKS5, scrape_info))

        proxy_dict = ProxyHelper.create_and_get_proxy_stats(tasks.results)

        logging.info(f'Successful: {len(proxy_dict["proxies"])}/{len(tasks.results)} || '
                     f'[Attempted HTTP: {len(http_scrape_info)} and HTTPS: {len(https_scrape_info)} and HTTP/S: {len(http_https_scrape_info)}] out of which [HTTP: {proxy_dict["http_count"]}] | [HTTPS: {proxy_dict["https_count"]}] | [HTTP/S: {proxy_dict["http_https_count"]}] || '
                     f'[Attempted SOCKS4: {len(socks4_scrape_info)} and SOCKS5: {len(socks5_scrape_info)} and SOCKS4/5: {len(socks4_socks5_scrape_info)}] out of which [SOCKS4: {proxy_dict["socks4_count"]}] | [SOCKS5: {proxy_dict["socks5_count"]}] | [SOCKS4/5: {proxy_dict["socks4_socks5_count"]}] ||')

        isps, locations = self._geo_repo.geo_resolve(proxy_dict["proxies"])

        await self._sql_repo.insert_proxies(isps, locations, proxy_dict["proxies"], Provider.PLDOWN)