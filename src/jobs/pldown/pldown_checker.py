import asyncio
from aiohttp import ClientSession
from contracts.enums import ProxyType, ScrapeProxyType, Provider
from utils.proxy_helper import ProxyHelper


class PldownChecker:

    def __init__(self, config, geo_repo, proxy_repo, sql_repo, api_repo, pldown_scraper):
        self._config = config
        self._geo_repo = geo_repo
        self._proxy_repo = proxy_repo
        self._sql_repo = sql_repo
        self._api_repo = api_repo
        self._pldown_scraper = pldown_scraper

    async def check_proxies(self):
        async with ClientSession() as client_session:
            pldown_http_task = asyncio.create_task(self._pldown_scraper.scrape(client_session, ScrapeProxyType.HTTP))
            pldown_http_ssl_task = asyncio.create_task(self._pldown_scraper.scrape(client_session, ScrapeProxyType.HTTPS))
            pldown_socks4_task = asyncio.create_task(self._pldown_scraper.scrape(client_session, ScrapeProxyType.SOCKS4))
            pldown_socks5_task = asyncio.create_task(self._pldown_scraper.scrape(client_session, ScrapeProxyType.SOCKS5))
            provider_proxies = await asyncio.gather(*[pldown_http_task, pldown_http_ssl_task, pldown_socks4_task, pldown_socks5_task])

        http_only = provider_proxies[0].difference(provider_proxies[1])

        set_proxies = [http_only, provider_proxies[1], provider_proxies[2], provider_proxies[3]]

        checked_proxies = await self._proxy_repo.check_proxies(set_proxies)

        proxies = ProxyHelper.create_and_log_proxy_stats(provider_proxies, checked_proxies, Provider.PLDOWN.value)

        isps, locations, geo_filtered_proxies = self._geo_repo.geo_resolve(proxies, get_country=False)

        await self._sql_repo.insert_proxies(isps, locations, geo_filtered_proxies, Provider.PLDOWN)

        await self._api_repo.cache_refresh()
