import os
import logging


class Base:
    isdevelopment = False
    isproduction = False
    provider_connections = dict(
        pldown='https://www.proxy-list.download',
        proxyscrape='https://api.proxyscrape.com/?request=displayproxies'
    )
    proxyscrape_pool_amount = 2000
    pldown_pool_amount = 2000


class DevelopmentConfig(Base):
    isdevelopment = True
    sql = dict(
        host='localhost',
        port='5432',
        database='proxydb',
        user='postgres',
        password='devpassword'
    )
    geo_db = dict(
        city_db='/app/src/data/GeoLite2-City.mmdb',
        asn_db='/app/src/data/GeoLite2-ASN.mmdb'
    )
    proxyscrape_pool_amount = 500


class ProductionConfig(Base):
    isproduction = True
    #change to PROD db url
    sql = dict(
        host='localhost',
        port='5432',
        database='proxydb',
        user='postgres',
        password='devpassword'
    )
    geo_db = dict(
        city_db='/app/src/data/GeoLite2-City.mmdb',
        asn_db='/app/src/data/GeoLite2-ASN.mmdb'
    )


class Config:
    settings: Base

    @classmethod
    def set_config(cls):
        try:
            env = os.environ["PSC-SETTINGS"]
        except KeyError:
            logging.fatal('Environment variable not set!')
            raise KeyError

        cls.settings = DevelopmentConfig() if env == 'Development' else ProductionConfig()
