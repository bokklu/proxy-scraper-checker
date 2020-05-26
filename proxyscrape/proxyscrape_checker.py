import asyncio
import logging
from aiohttp import ClientSession
from repositories.geo_repo import GeoRepo
from repositories.sql_repo import SqlRepo
from repositories.proxy_repo import ProxyRepo
from contracts.enums import ProxyType, Provider
from proxyscrape.proxyscrape_scraper import ProxyScrapeScraper
from dataclasses import dataclass
from utils.task_pool import TaskPool
from utils.proxy_helper import ProxyHelper


@dataclass
class ProxyScrapeChecker:
    _geo_repo: GeoRepo = GeoRepo(get_country=True)
    _proxyscrape_scraper: ProxyScrapeScraper = ProxyScrapeScraper()
    _proxy_repo: ProxyRepo = ProxyRepo(get_access_type=True)
    _sql_repo: SqlRepo = SqlRepo()

    async def check_proxies(self):
        async with ClientSession() as client_session:
            proxyscrape_http_task = asyncio.create_task(self._proxyscrape_scraper.scrape(client_session, ProxyType.HTTP))
            proxyscrape_socks4_task = asyncio.create_task(self._proxyscrape_scraper.scrape(client_session, ProxyType.SOCKS4))
            proxyscrape_socks5_task = asyncio.create_task(self._proxyscrape_scraper.scrape(client_session, ProxyType.SOCKS5))
            provider_proxies = await asyncio.gather(*[proxyscrape_http_task, proxyscrape_socks4_task, proxyscrape_socks5_task])

        socks4_proxies = provider_proxies[1] - provider_proxies[2]

        async with TaskPool(2000) as tasks:
            for scrape_info in provider_proxies[0]: await tasks.put(self._proxy_repo.ping_multiple_http(scrape_info))
            for scrape_info in socks4_proxies: await tasks.put(self._proxy_repo.ping_socks(ProxyType.SOCKS4, scrape_info))
            for scrape_info in provider_proxies[2]: await tasks.put(self._proxy_repo.ping_multiple_socks(scrape_info))

        proxy_dict = ProxyHelper.create_and_get_proxy_stats(tasks.results)

        logging.info(f'Successful Proxies: {len(proxy_dict["proxies"])}/{len(tasks.results)} || '
                     f'[Attempted HTTP/S: {len(provider_proxies[0])}] out of which [HTTP: {proxy_dict["http_count"]}] | [HTTPS: {proxy_dict["https_count"]}] | [HTTP/S: {proxy_dict["http_https_count"]}] || '
                     f'[Attempted SOCKS4: {len(socks4_proxies)} and SOCKS4/5: {len(provider_proxies[2])}] out of which [SOCKS4: {proxy_dict["socks4_count"]}] | [SOCKS5: {proxy_dict["socks5_count"]}] | [SOCKS4/5: {proxy_dict["socks4_socks5_count"]}] ||')

        isps, locations = self._geo_repo.geo_resolve(proxy_dict['proxies'])

        await self._sql_repo.insert_proxies(isps, locations, proxy_dict["proxies"], Provider.PROXYSCRAPE)
