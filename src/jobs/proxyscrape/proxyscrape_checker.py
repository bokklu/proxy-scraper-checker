import asyncio
from aiohttp import ClientSession
from contracts.enums import ScrapeProxyType, ProxyType, Provider
from utils.proxy_helper import ProxyHelper
from contracts.scrape_info import ScrapeInfo
import threading
from utils.task_pool import TaskPool
from aiosocks.connector import ProxyConnector, ProxyClientRequest


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

        self.split_proxies_threads(read_proxies)

        #checked_proxies = await self._proxy_repo.check_proxies(read_proxies)

        #proxies = ProxyHelper.create_and_log_proxy_stats(read_proxies, checked_proxies, Provider.PROXYSCRAPE.value)

        #isps, locations, geo_filtered_proxies = self._geo_repo.geo_resolve(proxies, get_country=True)

        #await self._sql_repo.insert_proxies(isps, locations, geo_filtered_proxies, Provider.PROXYSCRAPE)

        await self._api_repo.cache_refresh()

    def split_proxies_threads(self, all_proxies):
        # create 2 new threads

        t1 = threading.Thread(name='thread_check_proxies_split_one', target=self.thread_check_proxies_split_one,
                              args=[all_proxies])
        t2 = threading.Thread(name='thread_check_proxies_split_two', target=self.thread_check_proxies_split_two,
                              args=[all_proxies])

        t1.start()
        t2.start()
        t1.join()
        t2.join()

    def thread_check_proxies_split_one(self, split_proxies):
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(self.run_tasks_one(split_proxies))

    def thread_check_proxies_split_two(self, split_proxies):
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(self.run_tasks_two(split_proxies))

    async def run_tasks_one(self, split_proxies):
        socks_1_list = list(split_proxies[2])
        socks4_1 = socks_1_list[:798]

        connector = ProxyConnector(remote_resolve=False, limit=None, force_close=True)
        async with ClientSession(connector=connector, request_class=ProxyClientRequest) as session, TaskPool(875) as tasks:
            for scrape_info in split_proxies[0]: await tasks.put(self._proxy_repo.ping(session, ProxyType.HTTP, scrape_info))
            for scrape_info in split_proxies[1]: await tasks.put(self._proxy_repo.ping(session, ProxyType.HTTP, scrape_info, ssl=True))
            for scrape_info in socks4_1: await tasks.put(self._proxy_repo.ping(session, ProxyType.SOCKS4, scrape_info))

        ProxyHelper.create_and_log_proxy_stats(split_proxies, tasks.results, Provider.PROXYSCRAPE.value)

    async def run_tasks_two(self, split_proxies):
        socks_2_list = list(split_proxies[2])
        socks4_2 = socks_2_list[798:]

        connector = ProxyConnector(remote_resolve=False, limit=None, force_close=True)
        async with ClientSession(connector=connector, request_class=ProxyClientRequest) as session, TaskPool(875) as tasks:
            for scrape_info in socks4_2: await tasks.put(self._proxy_repo.ping(session, ProxyType.SOCKS4, scrape_info))
            for scrape_info in split_proxies[3]: await tasks.put(self._proxy_repo.ping(session, ProxyType.SOCKS5, scrape_info))

        ProxyHelper.create_and_log_proxy_stats(split_proxies, tasks.results, Provider.PROXYSCRAPE.value)