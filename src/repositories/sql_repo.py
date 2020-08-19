import asyncpg
import json
import logging


class SqlRepo:

    def __init__(self, config):
        self._config = config

    async def insert_proxies(self, isps, cities, proxies, provider):
        json_udts = self.convert_to_json(isps, cities, proxies)

        try:
            conn = await asyncpg.connect(host=self._config['sql']['host'], port=self._config['sql']['port'],
                                         database=self._config['sql']['database'], user=self._config['sql']['user'],
                                         password=self._config['sql']['password'])

            async with conn.transaction():
                insert_counts = await conn.fetchval('SELECT fn_insert_proxies($1, $2, $3)', json_udts[0], json_udts[1], json_udts[2])

            await conn.close()

            logging.info(f'{self.insert_proxies.__name__} for Provider: {provider.name}, '
                         f'inserted {insert_counts["insert_proxy_count"]} new proxy rows, '
                         f'updated {insert_counts["update_proxy_count"]} existing proxy rows, '
                         f'inserted {insert_counts["insert_city_count"]} new city rows, '
                         f'inserted {insert_counts["insert_isp_count"]} new isp rows.')
        except Exception as ex:
            logging.error(f'{self.insert_proxies.__name__} for Provider: {provider.name}, failed with ex: {str(ex)}')

    async def cleanup_proxies(self):
        try:
            conn = await asyncpg.connect(host=self._config['sql']['host'], port=self._config['sql']['port'],
                                         database=self._config['sql']['database'], user=self._config['sql']['user'],
                                         password=self._config['sql']['password'])

            async with conn.transaction():
                deleted_records = await conn.fetchval('SELECT fn_cleanup_proxies()')

            await conn.close()

            logging.info(f'{self.cleanup_proxies.__name__}, cleaned up {deleted_records["proxy_count"]} proxy rows, '
                         f'{deleted_records["city_count"]} city rows, {deleted_records["isp_count"]} isp rows.')

        except Exception as ex:
            logging.error(f'{self.cleanup_proxies.__name__}, failed with ex: {str(ex)}')

    @staticmethod
    def convert_to_json(isps, cities, proxies):
        json_isps = json.dumps([isp.__dict__ for isp in isps])
        json_cities = json.dumps([city.__dict__ for city in cities])
        json_proxies = json.dumps([proxy.__dict__ for proxy in proxies])

        return json_isps, json_cities, json_proxies
