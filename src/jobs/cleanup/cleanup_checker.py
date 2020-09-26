import logging
from contracts.enums import ProxyType
from contracts.scrape_info import ScrapeInfo
from utils.task_pool import TaskPool
from utils.proxy_helper import ProxyHelper
from contracts.proxy import Proxy


class CleanupChecker:

    def __init__(self, config, sql_repo, proxy_repo):
        self._config = config
        self._sql_repo = sql_repo
        self._proxy_repo = proxy_repo

    async def cleanup_proxies(self):
        cleanup_proxy_records = await self._sql_repo.get_cleanup_proxies()

        if len(cleanup_proxy_records) == 0:
            return

        http_proxies, https_proxies, http_https_proxies, socks4_proxies, socks5_proxies, socks4_socks5_proxies = [], [], [], [], [], []

	    self._proxy_repo.get_access_type = True

        for proxy_record in cleanup_proxy_records:
            proxy_type = proxy_record[0][2]
            scrape_info = ScrapeInfo(proxy=f'{proxy_record[0][0]}:{proxy_record[0][1]}', country_code=proxy_record[0][3])

            if proxy_type == ProxyType.HTTP.value:
                http_proxies.append(scrape_info)
                continue
            elif proxy_type == ProxyType.HTTPS.value:
                https_proxies.append(scrape_info)
                continue
            elif proxy_type == ProxyType.HTTP_HTTPS.value:
                http_https_proxies.append(scrape_info)
                continue
            elif proxy_type == ProxyType.SOCKS4.value:
                socks4_proxies.append(scrape_info)
                continue
            elif proxy_type == ProxyType.SOCKS5.value:
                socks5_proxies.append(scrape_info)
                continue
            elif proxy_type == ProxyType.SOCKS4_SOCKS5.value:
                socks4_socks5_proxies.append(scrape_info)
                continue

        async with TaskPool(self._config['cleanup_pool_amount']) as tasks:
            for scrape_info in http_proxies: await tasks.put(self._proxy_repo.ping_http(ProxyType.HTTP, scrape_info))
            for scrape_info in https_proxies: await tasks.put(self._proxy_repo.ping_http(ProxyType.HTTPS, scrape_info))
            for scrape_info in http_https_proxies: await tasks.put(self._proxy_repo.ping_multiple_http(scrape_info))
            for scrape_info in socks4_proxies: await tasks.put(self._proxy_repo.ping_socks(ProxyType.SOCKS4, scrape_info))
            for scrape_info in socks5_proxies: await tasks.put(self._proxy_repo.ping_socks(ProxyType.SOCKS5, scrape_info))
            for scrape_info in socks4_socks5_proxies: await tasks.put(self._proxy_repo.ping_multiple_socks(scrape_info))

        proxy_dict = ProxyHelper.create_and_get_proxy_stats(tasks.results, provider_id=None)

        if len(proxy_dict['proxies']) == 0:
            logging.info('Clean up job found no working proxies.')
            return

        logging.info(f'Successful: {len(proxy_dict["proxies"])}/{len(tasks.results)} || '
                     f'[Attempted HTTP: {len(http_proxies)} and HTTPS: {len(https_proxies)} and HTTP/S: {len(http_https_proxies)}] out of which [HTTP: {proxy_dict["http_count"]}] | [HTTPS: {proxy_dict["https_count"]}] | [HTTP/S: {proxy_dict["http_https_count"]}] || '
                     f'[Attempted SOCKS4: {len(socks4_proxies)} and SOCKS5: {len(socks5_proxies)} and SOCKS4/5: {len(socks4_socks5_proxies)}] out of which [SOCKS4: {proxy_dict["socks4_count"]}] | [SOCKS5: {proxy_dict["socks5_count"]}] | [SOCKS4/5: {proxy_dict["socks4_socks5_count"]}] ||')

        await self._sql_repo.cleanup_proxies(proxy_dict['proxies'])
