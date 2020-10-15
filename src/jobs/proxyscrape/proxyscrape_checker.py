import asyncio
import logging
import threading
from aiohttp import ClientSession
from contracts.enums import ProxyType, Provider
from contracts.scrape_info import ScrapeInfo
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



        provider_proxies = [http_proxies, https_proxies, socks4_proxies, socks5_proxies]

        self.split_proxies_threads(provider_proxies)


    def split_proxies_threads(self, all_proxies):
        #create 2 new threads

        t1 = threading.Thread(name='thread_check_proxies_split_one', target=self.thread_check_proxies_split_one, args=[all_proxies])
        t2 = threading.Thread(name='thread_check_proxies_split_two', target=self.thread_check_proxies_split_two, args=[all_proxies])

        t1.start()
        t2.start()
        t1.join()
        t2.join()

    def thread_check_proxies_split_one(self, split_proxies):
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(self.run_tasks_one(split_proxies))

    async def run_tasks_one(self, split_proxies):
        socks_1_list = list(split_proxies[2])
        socks4_1 = socks_1_list[:798]

        async with TaskPool(self._config['proxyscrape_pool_amount']) as tasks:
            for scrape_info in split_proxies[0]: await tasks.put(self._proxy_repo.ping_http(ProxyType.HTTP, scrape_info))
            for scrape_info in split_proxies[1]: await tasks.put(self._proxy_repo.ping_http(ProxyType.HTTPS, scrape_info))
            for scrape_info in socks4_1: await tasks.put(self._proxy_repo.ping_socks(ProxyType.SOCKS4, scrape_info))

        proxy_dict = ProxyHelper.create_and_get_proxy_stats(tasks.results, Provider.PROXYSCRAPE.value)

        logging.info(f'Successful: {len(proxy_dict["proxies"])}/{len(tasks.results)} || '
                     f'[Attempted HTTP: {len(split_proxies[0])} and HTTPS: {len(split_proxies[1])}] out of which [HTTP: {proxy_dict["http_count"]}] | [HTTPS: {proxy_dict["https_count"]}] || '
                     f'[Attempted SOCKS4_1: {len(socks4_1)}] out of which [SOCKS4: {proxy_dict["socks4_count"]}] ||')

    def thread_check_proxies_split_two(self, split_proxies):
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(self.run_tasks_two(split_proxies))

    async def run_tasks_two(self, split_proxies):
        socks_2_list = list(split_proxies[2])
        socks4_2 = socks_2_list[798:]

        async with TaskPool(self._config['proxyscrape_pool_amount']) as tasks:
            for scrape_info in socks4_2: await tasks.put(self._proxy_repo.ping_socks(ProxyType.SOCKS4, scrape_info))
            for scrape_info in split_proxies[3]: await tasks.put(self._proxy_repo.ping_socks(ProxyType.SOCKS5, scrape_info))

        proxy_dict = ProxyHelper.create_and_get_proxy_stats(tasks.results, Provider.PROXYSCRAPE.value)

        logging.info(f'Successful: {len(proxy_dict["proxies"])}/{len(tasks.results)} || '
                     f'[Attempted SOCKS4_2: {len(socks4_2)} and SOCKS5: {len(split_proxies[3])}] out of which [SOCKS4: {proxy_dict["socks4_count"]}] | [SOCKS5: {proxy_dict["socks5_count"]}] ||')
