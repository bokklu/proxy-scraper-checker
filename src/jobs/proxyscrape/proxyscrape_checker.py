import asyncio
from aiohttp import ClientSession
from contracts.enums import ScrapeProxyType, ProxyType, Provider
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
        async with ClientSession() as client_session:
            proxyscrape_http_task = asyncio.create_task(self._proxyscrape_scraper.scrape(client_session, ScrapeProxyType.HTTP))
            proxyscrape_http_ssl_task = asyncio.create_task(self._proxyscrape_scraper.scrape(client_session, ScrapeProxyType.HTTPS))
            proxyscrape_socks4_task = asyncio.create_task(self._proxyscrape_scraper.scrape(client_session, ScrapeProxyType.SOCKS4))
            proxyscrape_socks5_task = asyncio.create_task(self._proxyscrape_scraper.scrape(client_session, ScrapeProxyType.SOCKS5))

            provider_proxies = await asyncio.gather(*[proxyscrape_http_task, proxyscrape_http_ssl_task,
                                                      proxyscrape_socks4_task, proxyscrape_socks5_task])

        self._proxy_repo.get_access_type = True

        checked_proxies = await self._proxy_repo.check_proxies(provider_proxies)

        proxies = ProxyHelper.create_and_log_proxy_stats(provider_proxies, checked_proxies, Provider.PROXYSCRAPE.value)

        isps, locations, geo_filtered_proxies = self._geo_repo.geo_resolve(proxies, get_country=True)

        await self._sql_repo.insert_proxies(isps, locations, geo_filtered_proxies, Provider.PROXYSCRAPE)

        await self._api_repo.cache_refresh()
