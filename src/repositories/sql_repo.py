import asyncpg
import json
import logging


class SqlRepo:

    def __init__(self, config):
        self._config = config

    async def insert_proxies(self, isps, cities, proxies, provider):
        json_isps = json.dumps([isp.__dict__ for isp in isps])
        json_cities = json.dumps([city.__dict__ for city in cities])
        json_proxies = json.dumps([proxy.__dict__ for proxy in proxies])

        try:
            conn = await self._connect()

            async with conn.transaction():
                insert_counts = await conn.fetchval('SELECT fn_insert_proxies($1, $2, $3)', json_isps, json_cities, json_proxies)

            await conn.close()

            logging.info(f'{self.insert_proxies.__name__} for Provider: {provider.name}, '
                         f'inserted {insert_counts["insert_proxy_count"]} new proxy rows, '
                         f'updated {insert_counts["update_proxy_count"]} existing proxy rows, '
                         f'inserted {insert_counts["insert_city_count"]} new city rows, '
                         f'inserted {insert_counts["insert_isp_count"]} new isp rows.')
        except Exception as ex:
            logging.error(f'{self.insert_proxies.__name__} for Provider: {provider.name}, failed with ex: {str(ex)}')

    async def get_cleanup_proxies(self):
        try:
            conn = await self._connect()

            cleanup_proxies = await conn.fetch('SELECT fn_get_cleanup_proxies($1)', self._config['cleanup_hour_range'])

            await conn.close()

            logging.info(f'{self.get_cleanup_proxies.__name__} got {len(cleanup_proxies)} with cleanup-range of {self._config["cleanup_hour_range"]} hours')

            return cleanup_proxies

        except Exception as ex:
            logging.error(f'{self.get_cleanup_proxies.__name__}, failed with ex: {str(ex)}')

    async def cleanup_proxies(self, proxies):
        json_proxies = json.dumps([proxy.__dict__ for proxy in proxies])

        try:
            conn = await self._connect()

            async with conn.transaction():
                cleanup_count = await conn.fetchval('SELECT fn_cleanup_proxies($1)', json_proxies)

            await conn.close()

            logging.info(f'{self.cleanup_proxies.__name__}, cleaned up {cleanup_count["proxy_count"]} proxy rows, '
                         f'{cleanup_count["city_count"]} city rows, {cleanup_count["isp_count"]} isp rows.')

        except Exception as ex:
            logging.error(f'{self.cleanup_proxies.__name__}, failed with ex: {str(ex)}')

    def _connect(self):
        return asyncpg.connect(host=self._config['sql']['host'], port=self._config['sql']['port'],
                               database=self._config['sql']['database'], user=self._config['sql']['user'],
                               password=self._config['sql']['password'])

