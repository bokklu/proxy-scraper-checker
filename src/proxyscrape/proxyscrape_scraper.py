import asyncio
import logging
import async_timeout
from config import provider_connections
from contracts.scrape_info import ScrapeInfo
from dataclasses import dataclass


@dataclass
class ProxyScrapeScraper:

    @staticmethod
    async def scrape(session, proxy_type):
        for retry in range(3):
            try:
                async with async_timeout.timeout(7):
                    async with session.get(f'{provider_connections["proxyscrape"]}&proxytype={str.lower(proxy_type.name)}') as response:
                        content = await response.text()
                        content_set = content.splitlines()
                        return set(ScrapeInfo(proxy=x) for x in content_set)
            except asyncio.TimeoutError:
                logging.error('ProxyScrape Scraper connection timed out...')
                continue
            except Exception as ex:
                logging.error(f'ProxyScrape Scraper Exception: {str(ex)}')
                raise ex
