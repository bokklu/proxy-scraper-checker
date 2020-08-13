provider_connections = dict(
    pldown='https://www.proxy-list.download',
    proxyscrape='https://api.proxyscrape.com/?request=displayproxies'
)

sql = dict(
    host='db',
    port='5432',
    database='proxydb',
    user='postgres',
    password='devpassword'
)

geo_db = dict(
    city_db='/app/src/data/GeoLite2-City.mmdb',
    asn_db='/app/src/data/GeoLite2-ASN.mmdb'
)
