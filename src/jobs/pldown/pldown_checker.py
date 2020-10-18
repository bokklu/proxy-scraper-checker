import asyncio
import logging
from aiohttp import ClientSession
from contracts.enums import ProxyType, ScrapeProxyType, Provider
from utils.task_pool import TaskPool
from utils.proxy_helper import ProxyHelper


class PldownChecker:

    def __init__(self, config, geo_repo, proxy_repo, sql_repo, api_repo, pldown_scraper):
        self._config = config
        self._geo_repo = geo_repo
        self._proxy_repo = proxy_repo
        self._sql_repo = sql_repo
        self._api_repo = api_repo
        self._pldown_scraper = pldown_scraper

    async def check_proxies(self):
        async with ClientSession() as client_session:
            pldown_http_task = asyncio.create_task(self._pldown_scraper.scrape(client_session, ScrapeProxyType.HTTP))
            pldown_http_ssl_task = asyncio.create_task(self._pldown_scraper.scrape(client_session, ScrapeProxyType.HTTPS))
            pldown_socks4_task = asyncio.create_task(self._pldown_scraper.scrape(client_session, ScrapeProxyType.SOCKS4))
            pldown_socks5_task = asyncio.create_task(self._pldown_scraper.scrape(client_session, ScrapeProxyType.SOCKS5))
            provider_proxies = await asyncio.gather(*[pldown_http_task, pldown_http_ssl_task, pldown_socks4_task, pldown_socks5_task])

        http_only = provider_proxies[0].difference(provider_proxies[1])

        async with TaskPool(self._config['pldown_pool_amount']) as tasks:
            for scrape_info in http_only: await tasks.put(self._proxy_repo.ping_http(ProxyType.HTTP, scrape_info))
            for scrape_info in provider_proxies[1]: await tasks.put(self._proxy_repo.ping_http(ProxyType.HTTP, scrape_info, ssl=True))
            for scrape_info in provider_proxies[2]: await tasks.put(self._proxy_repo.ping_socks(ProxyType.SOCKS4, scrape_info))
            for scrape_info in provider_proxies[3]: await tasks.put(self._proxy_repo.ping_socks(ProxyType.SOCKS5, scrape_info))

        proxy_dict = ProxyHelper.create_and_get_proxy_stats(tasks.results, Provider.PLDOWN.value)

        logging.info(f'Successful: {len(proxy_dict["proxies"])}/{len(tasks.results)} || '
                     f'[Attempted HTTP: {len(provider_proxies[0])} and HTTPS: {len(provider_proxies[1])}] out of which [HTTP: {proxy_dict["http_count"]}] | [HTTPS: {proxy_dict["https_count"]}] || '
                     f'[Attempted SOCKS4: {len(provider_proxies[2])} and SOCKS5: {len(provider_proxies[3])}] out of which [SOCKS4: {proxy_dict["socks4_count"]}] | [SOCKS5: {proxy_dict["socks5_count"]}] ||')

        isps, locations, geo_filtered_proxies = self._geo_repo.geo_resolve(proxy_dict["proxies"], get_country=False)

        await self._sql_repo.insert_proxies(isps, locations, geo_filtered_proxies, Provider.PLDOWN)

        await self._api_repo.cache_refresh()
