import asyncio
import logging
from aiohttp import ClientSession
from contracts.scrape_info import ScrapeInfo
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
        self._proxy_repo.get_access_type = True

        http_proxies_file = open("proxyscrape-proxies-http.txt", "r")
        https_proxies_file = open("proxyscrape-proxies-https.txt", "r")
        socks4_proxies_file = open("proxyscrape-proxies-socks4.txt", "r")
        socks5_proxies_file = open("proxyscrape-proxies-socks5.txt", "r")

        http_proxies = []
        https_proxies = []
        socks4_proxies = []
        socks5_proxies = []

        for proxy in http_proxies_file: http_proxies.append(ScrapeInfo(proxy=proxy.rstrip('\n')))
        for proxy in https_proxies_file: https_proxies.append(ScrapeInfo(proxy=proxy.rstrip('\n')))
        for proxy in socks4_proxies_file: socks4_proxies.append(ScrapeInfo(proxy=proxy.rstrip('\n')))
        for proxy in socks5_proxies_file: socks5_proxies.append(ScrapeInfo(proxy=proxy.rstrip('\n')))

        async with TaskPool(self._config['proxyscrape_pool_amount']) as tasks:
            for scrape_info in http_proxies: await tasks.put(self._proxy_repo.ping_http(ProxyType.HTTP, scrape_info))
            for scrape_info in https_proxies: await tasks.put(self._proxy_repo.ping_http(ProxyType.HTTPS, scrape_info))
            for scrape_info in socks4_proxies: await tasks.put(self._proxy_repo.ping_socks(ProxyType.SOCKS4, scrape_info))
            for scrape_info in socks5_proxies: await tasks.put(self._proxy_repo.ping_socks(ProxyType.SOCKS5, scrape_info))

        proxy_dict = ProxyHelper.create_and_get_proxy_stats(tasks.results, Provider.PROXYSCRAPE.value)

        logging.info(f'Successful: {len(proxy_dict["proxies"])}/{len(tasks.results)} || '
                     f'[Attempted HTTP: {len(http_proxies)} and HTTPS: {len(https_proxies)}] out of which [HTTP: {proxy_dict["http_count"]}] | [HTTPS: {proxy_dict["https_count"]}] || '
                     f'[Attempted SOCKS4: {len(socks4_proxies)} and SOCKS5: {len(socks5_proxies)}] out of which [SOCKS4: {proxy_dict["socks4_count"]}] | [SOCKS5: {proxy_dict["socks5_count"]}] ||')

        isps, locations, geo_filtered_proxies = self._geo_repo.geo_resolve(proxy_dict['proxies'], get_country=True)

        await self._sql_repo.insert_proxies(isps, locations, geo_filtered_proxies, Provider.PROXYSCRAPE)

        await self._api_repo.cache_refresh()
