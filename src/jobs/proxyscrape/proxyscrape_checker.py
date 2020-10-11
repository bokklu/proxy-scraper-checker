import asyncio
import logging
from aiohttp import ClientSession
from contracts.enums import ProxyType, Provider
from utils.task_pool import TaskPool
from utils.proxy_helper import ProxyHelper


class ProxyScrapeChecker:

    def __init__(self, config, geo_repo, proxy_repo, sql_repo, api_repo, proxyscrape_scraper):
        self._config = config
        self._geo_repo = geo_repo
        self._proxy_repo = proxy_repo
        self._sql_repo = sql_repo
        self._api_repo = api_repo
        self._proxyscrape_scraper = proxyscrape_scraper

    async def check_proxies(self):
        async with ClientSession() as client_session:
            proxyscrape_http_task = asyncio.create_task(self._proxyscrape_scraper.scrape(client_session, ProxyType.HTTP))
            proxyscrape_socks4_task = asyncio.create_task(self._proxyscrape_scraper.scrape(client_session, ProxyType.SOCKS4))
            proxyscrape_socks5_task = asyncio.create_task(self._proxyscrape_scraper.scrape(client_session, ProxyType.SOCKS5))
            provider_proxies = await asyncio.gather(*[proxyscrape_http_task, proxyscrape_socks4_task, proxyscrape_socks5_task])

        # check ips which are in http/https and also socks4/5 [and remove them from socks]
        http_socks4 = provider_proxies[0].intersection(provider_proxies[1])
        http_socks5 = provider_proxies[0].intersection(provider_proxies[2])
        provider_proxies[1].difference_update(http_socks4)
        provider_proxies[2].difference_update(http_socks5)

        socks4_proxies = provider_proxies[1] - provider_proxies[2]

        self._proxy_repo.get_access_type = True

        async with TaskPool(self._config['proxyscrape_pool_amount']) as tasks:
            for scrape_info in provider_proxies[0]: await tasks.put(self._proxy_repo.ping_multiple_http(scrape_info))
            for scrape_info in socks4_proxies: await tasks.put(self._proxy_repo.ping_socks(ProxyType.SOCKS4, scrape_info))
            for scrape_info in provider_proxies[2]: await tasks.put(self._proxy_repo.ping_multiple_socks(scrape_info))

        proxy_dict = ProxyHelper.create_and_get_proxy_stats(tasks.results, Provider.PROXYSCRAPE.value)

        logging.info(f'Successful Proxies: {len(proxy_dict["proxies"])}/{len(tasks.results)} || '
                     f'[Attempted HTTP/S: {len(provider_proxies[0])}] out of which [HTTP: {proxy_dict["http_count"]}] | [HTTPS: {proxy_dict["https_count"]}] | [HTTP/S: {proxy_dict["http_https_count"]}] || '
                     f'[Attempted SOCKS4: {len(socks4_proxies)} and SOCKS4/5: {len(provider_proxies[2])}] out of which [SOCKS4: {proxy_dict["socks4_count"]}] | [SOCKS5: {proxy_dict["socks5_count"]}] | [SOCKS4/5: {proxy_dict["socks4_socks5_count"]}] ||')

        isps, locations, geo_filtered_proxies = self._geo_repo.geo_resolve(proxy_dict['proxies'], get_country=True)

        await self._sql_repo.insert_proxies(isps, locations, geo_filtered_proxies, Provider.PROXYSCRAPE)

        await self._api_repo.cache_refresh()
