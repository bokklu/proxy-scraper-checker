class Base:
    isdevelopment = False
    isproduction = False
    provider_connections = dict(
        pldown='https://www.proxy-list.download',
        proxyscrape='https://api.proxyscrape.com/?request=displayproxies'
    )
    geo_db = dict(
        city_db='F:\Projects\proxy-scraper-checker\src\data\GeoLite2-City.mmdb',
        asn_db='F:\Projects\proxy-scraper-checker\src\data\GeoLite2-ASN.mmdb'
    )
    proxyscrape_pool_amount = 1750
    pldown_pool_amount = 5000
    max_retries = 3
    timeout = 8
    cache_api_timeout = 10
    cleanup_hour_range = 2
    cleanup_pool_amount = 5000


class DevelopmentConfig(Base):
    isdevelopment = True
    sql = dict(
        host='localhost',
        port='5432',
        database='proxydb',
        user='postgres',
        password='devpassword'
    )
    cache_api = 'http://localhost:5000/proxy/cacherefresh'

    def asdict(self):
        return dict(isdevelopment=self.isdevelopment, isproduction=super().isproduction,
                    provider_connections=super().provider_connections, sql=self.sql, cache_api=self.cache_api,
                    cache_api_timeout=super().cache_api_timeout, geo_db=self.geo_db,
                    proxyscrape_pool_amount=super().proxyscrape_pool_amount, pldown_pool_amount=super().pldown_pool_amount,
                    max_retries=super().max_retries, timeout=super().timeout, cleanup_hour_range=super().cleanup_hour_range,
                    cleanup_pool_amount=super().cleanup_pool_amount)


class ProductionConfig(Base):
    isproduction = True
    sql = dict(
        host='vmi449515.contaboserver.net',
        port='5432',
        database='proxydb',
        user='postgres'
    )
    cache_api = 'https://api.proxykingdom.com/proxy/cacherefresh'
    
    def asdict(self):
        return dict(isdevelopment=super().isdevelopment, isproduction=self.isproduction,
                    provider_connections=super().provider_connections, sql=self.sql, cache_api=self.cache_api,
                    cache_api_timeout=super().cache_api_timeout, geo_db=self.geo_db,
                    proxyscrape_pool_amount=super().proxyscrape_pool_amount, pldown_pool_amount=super().pldown_pool_amount,
                    max_retries=super().max_retries, timeout=super().timeout, cleanup_hour_range=super().cleanup_hour_range,
                    cleanup_pool_amount=super().cleanup_pool_amount)
