import asyncio
import logging
import async_timeout
from contracts.scrape_info import ScrapeInfo
from contracts.enums import ScrapeProxyType


class ProxyScrapeScraper:

    def __init__(self, config):
        self._config = config

    async def scrape(self, session, proxy_type):

        if proxy_type is ScrapeProxyType.HTTPS:
            ssl = 'yes'
            proxy_type = ScrapeProxyType.HTTP
        elif proxy_type is ScrapeProxyType.HTTP:
            ssl = 'no'
        else:
            ssl = 'all'

        for retry in range(10):
            try:
                async with async_timeout.timeout(7):
                    async with session.get(f'{self._config["provider_connections"]["proxyscrape"]}&proxytype={str.lower(proxy_type.name)}&ssl={ssl}') as response:
                        content = await response.text()
                        content_set = content.splitlines()
                        return set(ScrapeInfo(proxy=x) for x in content_set)
            except asyncio.TimeoutError:
                logging.error('ProxyScrape Scraper connection timed out...')
                continue
            except Exception as ex:
                logging.error(f'ProxyScrape Scraper Exception: {str(ex)}')
                raise ex
