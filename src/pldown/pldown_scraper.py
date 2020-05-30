import asyncio
import async_timeout
import config
import logging
from contracts.enums import ProxyAccessType
from contracts.scrape_info import ScrapeInfo
from dataclasses import dataclass


@dataclass
class PldownScraper:

    @staticmethod
    async def scrape(session, proxy_type):
        try:
            async with async_timeout.timeout(7):
                async with session.get(f'{config.provider_connections["pldown"]}/api/v0/get?l=en&t={str.lower(proxy_type.name)}') as response:
                    result = await response.json(content_type='text/html')
                    return set(ScrapeInfo(proxy=f'{x["IP"]}:{x["PORT"]}', country_code=x['ISO'], access_type_id=ProxyAccessType[x["ANON"]].value)
                               for x in result[0]["LISTA"] if x["ISO"] or x["ANON"] is not None)
        except asyncio.TimeoutError as timeout_ex:
            logging.error('Pldown Scraper connection timed out...')
            raise timeout_ex
        except Exception as ex:
            logging.error(f'Pldown Scraper Exception: {str(ex)}')
            raise ex
