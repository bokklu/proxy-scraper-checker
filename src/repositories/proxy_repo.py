import asyncio
import async_timeout
import aiohttp
import time
from aiohttp_socks import ProxyConnector, ProxyError
from src.contracts.statistics import Statistics
from src.contracts.enums import Response, ProxyAccessType, ProxyType


class ProxyRepo:

    def __init__(self, get_access_type):
        self.__get_access_type = get_access_type
        self.__timeout = 8
        self.__max_retries = 3

    async def ping_http(self, http_type, scrape_info):
        statistics = Statistics(type_id=http_type.value)
        async with aiohttp.ClientSession() as session:
            response_times = []
            for attempt in range(self.__max_retries):
                try:
                    async with async_timeout.timeout(self.__timeout):
                        req_start_time = time.time()
                        async with session.get(f'{http_type.name.lower()}://example.com', proxy=f'http://{scrape_info.proxy}', allow_redirects=False, verify_ssl=False) as response:
                            if response.status == 200 or response.status == 302:
                                response_times.append(int(round((time.time() - req_start_time) * 1000)))
                            else:
                                statistics.result_type = Response.OTHER
                                return statistics
                except asyncio.TimeoutError:
                    continue
                except (aiohttp.ServerDisconnectedError, OSError) as server_os_error:
                    print(f'{scrape_info.proxy} {http_type.name} Server/OS Error: {server_os_error}')
                    if attempt == self.__max_retries:
                        statistics.result_type = Response.ERROR
                        return statistics
                except (aiohttp.ClientProxyConnectionError, Exception) as break_ex:
                    print(f'{scrape_info.proxy} {http_type.name} Break Ex: {break_ex}')
                    statistics.result_type = Response.ERROR
                    return statistics

            if response_times:
                print(f'{scrape_info.proxy} for {http_type.name} is successful')
                ip_tokens = scrape_info.proxy.split(':')
                statistics.address = ip_tokens[0]
                statistics.port = ip_tokens[1]
                statistics.country_code = scrape_info.country_code
                statistics.result_type = Response.SUCCESS
                statistics.speed = int(sum(response_times) / len(response_times))
                statistics.uptime = len(response_times)
                statistics.access_type_id = self._check_access_type(response.headers) if self.__get_access_type else scrape_info.access_type_id
        return statistics

    async def ping_socks(self, socks_type, scrape_info):
        statistics = Statistics(type_id=socks_type.value)
        connector = ProxyConnector.from_url(f'{socks_type.name.lower()}://{scrape_info.proxy}')
        async with aiohttp.ClientSession(connector=connector) as client_session:
            response_times = []
            for attempt in range(self.__max_retries):
                try:
                    async with async_timeout.timeout(self.__timeout):
                        req_start_time = time.time()
                        async with client_session.get('http://example.com', allow_redirects=False) as response:
                            if response.status == 200 or response.status == 302:
                                response_times.append(int(round((time.time() - req_start_time) * 1000)))
                            else:
                                statistics.result_type = Response.OTHER
                                return statistics
                except asyncio.TimeoutError:
                    continue
                except (OSError, ProxyError) as error_ex:
                    print(f'{scrape_info.proxy} Error: {error_ex}')
                    if attempt == self.__max_retries:
                        statistics.result_type = Response.ERROR
                        return statistics
                except (aiohttp.ClientProxyConnectionError, Exception) as break_ex:
                    print(f'{scrape_info.proxy} Break Ex: {break_ex}')
                    statistics.result_type = Response.ERROR
                    return statistics

        if response_times:
            print(f'{scrape_info.proxy} is successful')
            ip_tokens = scrape_info.proxy.split(':')
            statistics.address = ip_tokens[0]
            statistics.port = ip_tokens[1]
            statistics.country_code = scrape_info.country_code
            statistics.result_type = Response.SUCCESS
            statistics.speed = int(sum(response_times) / len(response_times))
            statistics.uptime = len(response_times)
            statistics.access_type_id = self._check_access_type(response.headers) if self.__get_access_type else scrape_info.access_type_id

        return statistics

    async def ping_multiple_http(self, scrape_info):
        http_task = asyncio.create_task(self.ping_http(ProxyType.HTTP, scrape_info))
        https_task = asyncio.create_task(self.ping_http(ProxyType.HTTPS, scrape_info))
        results = await asyncio.gather(http_task, https_task)

        if results[0].result_type is Response.SUCCESS and results[1].result_type is Response.SUCCESS:
            results[0].type_id = ProxyType.HTTP_HTTPS.value
            return results[0]
        elif results[0].result_type is Response.SUCCESS and results[1].result_type is not Response.SUCCESS:
            return results[0]
        elif results[0].result_type is not Response.SUCCESS and results[1].result_type is Response.SUCCESS:
            return results[1]
        else:
            return results[0]

    async def ping_multiple_socks(self, scrape_info):
        socks4_task = asyncio.create_task(self.ping_socks(ProxyType.SOCKS4, scrape_info))
        socks5_task = asyncio.create_task(self.ping_socks(ProxyType.SOCKS5, scrape_info))
        results = await asyncio.gather(socks4_task, socks5_task)

        if results[0].result_type is Response.SUCCESS and results[1].result_type is Response.SUCCESS:
            results[0].type_id = ProxyType.SOCKS4_SOCKS5.value
            return results[0]
        elif results[0].result_type is Response.SUCCESS and results[1].result_type is not Response.SUCCESS:
            return results[0]
        elif results[0].result_type is not Response.SUCCESS and results[1].result_type is Response.SUCCESS:
            return results[1]
        else:
            return results[0]

    @staticmethod
    def _check_access_type(response_headers):
        if 'X-Cache-Lookup' and 'Via' in response_headers:
            return ProxyAccessType.TRANSPARENT.value
        elif ('Via' in response_headers and 'X-Cache-Lookup' not in response_headers) or ('X-Cache-Lookup' in response_headers and 'Via' not in response_headers):
            return ProxyAccessType.ANONYMOUS.value
        elif 'Via' and 'X-Cache-Lookup' not in response_headers:
            return ProxyAccessType.ELITE.value
