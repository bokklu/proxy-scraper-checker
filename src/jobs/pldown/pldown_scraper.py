import asyncio
import async_timeout
import logging
from contracts.enums import ProxyAccessType
from contracts.scrape_info import ScrapeInfo


class PldownScraper:

    def __init__(self, config):
        self._config = config

    async def scrape(self, session, proxy_type):
        for retry in range(10):
            try:
                async with async_timeout.timeout(7):
                    async with session.get(f'{self._config["provider_connections"]["pldown"]}/api/v0/get?l=en&t={str.lower(proxy_type.name)}') as response:
                        result = await response.json(content_type='text/html')
                        return set(ScrapeInfo(proxy=f'{x["IP"]}:{x["PORT"]}', country_code=x['ISO'], access_type_id=ProxyAccessType[x["ANON"]].value)
                                   for x in result[0]["LISTA"] if x["ISO"] or x["ANON"] is not None)
            except asyncio.TimeoutError:
                logging.error('Pldown Scraper connection timed out...')
                continue
            except Exception as ex:
                logging.error(f'Pldown Scraper Exception: {str(ex)}')
                raise ex
