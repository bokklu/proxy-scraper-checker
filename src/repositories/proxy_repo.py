import asyncio
import async_timeout
import aiohttp
from aiosocks.errors import SocksError
from contracts.statistics import Statistics
from contracts.enums import Response, ProxyAccessType, ProxyType
from aiosocks.connector import ProxyConnector, ProxyClientRequest
from utils.task_pool import TaskPool
import time


class ProxyRepo:

    def __init__(self, config):
        self._timeout = config['timeout']
        self._max_retries = config['max_retries']
        self._task_pool = config['task_pool']
        self.get_access_type = False

    async def check_proxies(self, provider_proxies):
        connector = ProxyConnector(remote_resolve=False, limit=None, force_close=True)
        #trace_config = aiohttp.TraceConfig()
        #trace_config.on_request_start.append(self._on_request_start)
        #trace_config.on_request_end.append(self._on_request_end)
        #trace_config.on_connection_create_end.append(self._on_connection_create_end)
        async with aiohttp.ClientSession(connector=connector, request_class=ProxyClientRequest) as session, TaskPool(self._task_pool) as tasks:
            for x in provider_proxies[0]: await tasks.put(self._ping(session, ProxyType.HTTP, x))
            for x in provider_proxies[1]: await tasks.put(self._ping(session, ProxyType.HTTP, x, ssl=True))
            for x in provider_proxies[2]: await tasks.put(self._ping(session, ProxyType.SOCKS4, x))
            for x in provider_proxies[3]: await tasks.put(self._ping(session, ProxyType.SOCKS5, x))

        return tasks.results

    async def ping(self, session, proxy_type, scrape_info, ssl=False):
        statistics = Statistics(type_id=proxy_type.value)
        req_start_time = time.time()
        response_times = []
        ssl = 'https' if ssl is True else 'http'
        for attempt in range(self._max_retries):
            try:
                async with async_timeout.timeout(self._timeout):
                    async with session.get(f'{ssl}://example.com',
                                           proxy=f'socks4://91.200.125.75:4145',
                                           allow_redirects=False, ssl=False) as response:
                        if response.status == 200 or response.status == 302:
                            response_times.append(int(round((time.time() - req_start_time) * 1000)))
                        else:
                            statistics.result_type = Response.OTHER
                            return statistics
            except asyncio.TimeoutError:
                continue
            except (aiohttp.ServerDisconnectedError, SocksError, OSError) as server_os_error:
                print(f'{scrape_info.proxy} {proxy_type.name} Server/OS Error: {server_os_error}')
                if attempt == self._max_retries - 1:
                    statistics.result_type = Response.ERROR
                    return statistics
            except aiohttp.ClientHttpProxyError as http_error:
                print(f'{scrape_info.proxy} {proxy_type.name} Http Error: {http_error}')
                statistics.result_type = Response.OTHER
                return statistics
            except (aiohttp.ClientProxyConnectionError, Exception) as break_ex:
                print(f'{scrape_info.proxy} {proxy_type.name} Break Ex: {break_ex}')
                statistics.result_type = Response.ERROR
                return statistics

        if response_times:
            print(f'{scrape_info.proxy} for {proxy_type.name} is successful')
            ip_tokens = scrape_info.proxy.split(':')
            statistics.address = ip_tokens[0]
            statistics.port = ip_tokens[1]
            statistics.country_code = scrape_info.country_code
            statistics.result_type = Response.SUCCESS
            statistics.speed = int(sum(response_times) / len(response_times))
            statistics.uptime = len(response_times)
            statistics.access_type_id = \
                self._check_access_type(response.headers) if self.get_access_type else scrape_info.access_type_id
            statistics.ssl = False if proxy_type is ProxyType.HTTP else True
            statistics.get = True
            statistics.post = True
        return statistics

    @staticmethod
    def _check_access_type(response_headers):
        if 'X-Cache-Lookup' and 'Via' in response_headers:
            return ProxyAccessType.TRANSPARENT.value
        elif ('Via' in response_headers and 'X-Cache-Lookup' not in response_headers) or ('X-Cache-Lookup' in response_headers and 'Via' not in response_headers):
            return ProxyAccessType.ANONYMOUS.value
        elif 'Via' and 'X-Cache-Lookup' not in response_headers:
            return ProxyAccessType.ELITE.value

    @staticmethod
    async def _on_request_start(session, trace_config_ctx, params):
        trace_config_ctx.start = asyncio.get_event_loop().time()

    @staticmethod
    async def _on_request_end(session, trace_config_ctx, params):
        elapsed = asyncio.get_event_loop().time() - trace_config_ctx.start
        #print("Request took {}".format(elapsed))

    @staticmethod
    async def _on_connection_create_end(session, trace_config_ctx, params):
        elapsed = asyncio.get_event_loop().time() - trace_config_ctx.start
        #print("Connection create start took {}".format(elapsed))
