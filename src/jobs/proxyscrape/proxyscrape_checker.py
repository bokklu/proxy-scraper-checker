import asyncio
from aiohttp import ClientSession
from contracts.enums import ScrapeProxyType, ProxyType, Provider
from utils.proxy_helper import ProxyHelper
from contracts.scrape_info import ScrapeInfo


class ProxyScrapeChecker:

    def __init__(self, config, geo_repo, proxy_repo, sql_repo, api_repo, proxyscrape_scraper):
        self._config = config
        self._geo_repo = geo_repo
        self._proxy_repo = proxy_repo
        self._sql_repo = sql_repo
        self._api_repo = api_repo
        self._proxyscrape_scraper = proxyscrape_scraper

    async def check_proxies(self):
        http_proxies_file = open("proxyscrape-http-proxies.txt", "r")
        https_proxies_file = open("proxyscrape-https-proxies.txt", "r")
        socks4_proxies_file = open("proxyscrape-socks4-proxies.txt", "r")
        socks5_proxies_file = open("proxyscrape-socks5-proxies.txt", "r")

        http_proxies = []
        https_proxies = []
        socks4_proxies = []
        socks5_proxies = []

        for proxy in http_proxies_file: http_proxies.append(ScrapeInfo(proxy=proxy.rstrip('\n')))
        for proxy in https_proxies_file: https_proxies.append(ScrapeInfo(proxy=proxy.rstrip('\n')))
        for proxy in socks4_proxies_file: socks4_proxies.append(ScrapeInfo(proxy=proxy.rstrip('\n')))
        for proxy in socks5_proxies_file: socks5_proxies.append(ScrapeInfo(proxy=proxy.rstrip('\n')))

        self._proxy_repo.get_access_type = True

        read_proxies = [http_proxies, https_proxies, socks4_proxies, socks5_proxies]

        checked_proxies = await self._proxy_repo.check_proxies(read_proxies)

        proxies = ProxyHelper.create_and_log_proxy_stats(read_proxies, checked_proxies, Provider.PROXYSCRAPE.value)

        isps, locations, geo_filtered_proxies = self._geo_repo.geo_resolve(proxies, get_country=True)

        await self._sql_repo.insert_proxies(isps, locations, geo_filtered_proxies, Provider.PROXYSCRAPE)

        await self._api_repo.cache_refresh()
