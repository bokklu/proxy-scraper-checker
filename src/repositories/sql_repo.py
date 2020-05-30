import asyncpg
import json
import logging
from config import sql
from dataclasses import dataclass


@dataclass
class SqlRepo:

    async def insert_proxies(self, isps, locations, proxies, provider):
        json_udts = self.convert_to_json(isps, locations, proxies)

        try:
            conn = await asyncpg.connect(host=sql['host'], port=sql['port'], database=sql['database'], user=sql['user'], password=sql['password'])

            async with conn.transaction():
                upsert_record = await conn.fetchval('SELECT fn_insert_proxies($1, $2, $3)', json_udts[0], json_udts[1], json_udts[2])

            await conn.close()

            logging.info(f'{self.insert_proxies.__name__} for Provider: {provider.name}, '
                         f'inserted {upsert_record["insert_count"]} new rows, updated {upsert_record["update_count"]}')
        except Exception as ex:
            logging.error(f'{self.insert_proxies.__name__} for Provider: {provider.name}, failed with ex: {str(ex)}')

    @staticmethod
    def convert_to_json(isps, locations, proxies):
        json_isps = json.dumps([isp.__dict__ for isp in isps])
        json_locations = json.dumps([location.__dict__ for location in locations])
        json_proxies = json.dumps([proxy.__dict__ for proxy in proxies])

        return json_isps, json_locations, json_proxies
