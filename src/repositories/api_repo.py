import aiohttp
import async_timeout
import uuid
import logging


class ApiRepo:

    def __init__(self, config):
        self._cache_api = config['cache_api']
        self._cache_api_timeout = config['cache_api_timeout']
        self._isdevelopment = config['isdevelopment']

    async def cache_refresh(self):
        correlation_id = str(uuid.uuid4())
        headers = {'correlation_id': correlation_id}

        if self._isdevelopment:
            headers['X-Forwarded-For'] = '127.0.0.1'

        async with aiohttp.ClientSession() as session:
            async with async_timeout.timeout(self._cache_api_timeout):
                async with session.put(self._cache_api, headers=headers, verify_ssl=False) as response:
                    if response.status == 200:
                        logging.info(f'Cache has been refreshed, CorrelationId={correlation_id}')
                    elif response.status != 200:
                        logging.error(f'Something went wrong when refreshing the cache, CorrelationId={correlation_id}')
                    return
