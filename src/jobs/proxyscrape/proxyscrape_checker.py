import asyncio
import logging
from aiohttp import ClientSession
from aiosocks.connector import ProxyConnector, ProxyClientRequest
from contracts.enums import ScrapeProxyType, ProxyType, Provider
from contracts.scrape_info import ScrapeInfo
from utils.proxy_helper import ProxyHelper
from utils.task_pool import TaskPool


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
            proxyscrape_http_task = asyncio.create_task(self._proxyscrape_scraper.scrape(client_session, ScrapeProxyType.HTTP))
            proxyscrape_http_ssl_task = asyncio.create_task(self._proxyscrape_scraper.scrape(client_session, ScrapeProxyType.HTTPS))
            proxyscrape_socks4_task = asyncio.create_task(self._proxyscrape_scraper.scrape(client_session, ScrapeProxyType.SOCKS4))
            proxyscrape_socks5_task = asyncio.create_task(self._proxyscrape_scraper.scrape(client_session, ScrapeProxyType.SOCKS5))

            provider_proxies = await asyncio.gather(*[proxyscrape_http_task, proxyscrape_http_ssl_task,
                                                      proxyscrape_socks4_task, proxyscrape_socks5_task])

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

        connector = ProxyConnector(remote_resolve=False, limit=None, verify_ssl=False)
        async with ClientSession(connector=connector, request_class=ProxyClientRequest) as session, TaskPool(1750) as tasks:
            for x in http_proxies: await tasks.put(self._proxy_repo.ping(session, ProxyType.HTTP, x))
            for x in https_proxies: await tasks.put(self._proxy_repo.ping(session, ProxyType.HTTP, x, ssl=True))
            for x in socks4_proxies: await tasks.put(self._proxy_repo.ping(session, ProxyType.SOCKS4, x))
            for x in socks5_proxies: await tasks.put(self._proxy_repo.ping(session, ProxyType.SOCKS5, x))

        proxy_dict = ProxyHelper.create_and_get_proxy_stats(tasks.results, Provider.PROXYSCRAPE.value)

        #logging.info(f'Successful: {len(proxy_dict["proxies"])}/{len(tasks.results)}\n'
        #             f'HTTP => [{proxy_dict["http_count"]}/{len(provider_proxies[0])}]\n'
        #             f'HTTP SSL => [{proxy_dict["http_ssl_count"]}/{len(provider_proxies[1])}]\n'
        #             f'SOCKS4 => [{proxy_dict["socks4_count"]}/{len(provider_proxies[2])}]\n'
        #             f'SOCKS5 => [{proxy_dict["socks5_count"]}/{len(provider_proxies[3])}]')

        logging.info(f'Successful: {len(proxy_dict["proxies"])}/{len(tasks.results)}\n'
                     f'HTTP => [{proxy_dict["http_count"]}/{len(http_proxies)}]\n'
                     f'HTTP SSL => [{proxy_dict["http_ssl_count"]}/{len(https_proxies)}]\n'
                     f'SOCKS4 => [{proxy_dict["socks4_count"]}/{len(socks4_proxies)}]\n'
                     f'SOCKS5 => [{proxy_dict["socks5_count"]}/{len(socks5_proxies)}]')

        isps, locations, geo_filtered_proxies = self._geo_repo.geo_resolve(proxy_dict['proxies'], get_country=True)

        #await self._sql_repo.insert_proxies(isps, locations, geo_filtered_proxies, Provider.PROXYSCRAPE)

        #await self._api_repo.cache_refresh()
