from src.contracts.enums import Response, ProxyType, Provider
from src.contracts.proxy import Proxy


class ProxyHelper:

    @staticmethod
    def create_and_get_proxy_stats(task_results):
        proxy_records = set()
        http_c = https_c = http_https_c = socks4_c = socks5_c = socks4_socks5_c = 0

        for t in task_results:

            if t.result_type is Response.SUCCESS:
                if t.type_id is ProxyType.HTTP.value: http_c += 1
                elif t.type_id is ProxyType.HTTPS.value: https_c += 1
                elif t.type_id is ProxyType.HTTP_HTTPS.value: http_https_c += 1
                elif t.type_id is ProxyType.SOCKS4.value: socks4_c += 1
                elif t.type_id is ProxyType.SOCKS5.value: socks5_c += 1
                elif t.type_id is ProxyType.SOCKS4_SOCKS5.value: socks4_socks5_c += 1

                proxy_records.add(Proxy(address=t.address, port=t.port, country_code=t.country_code,
                                           provider_id=Provider.PROXYSCRAPE.value,
                                           access_type_id=t.access_type_id, type_id=t.type_id, speed=t.speed,
                                           uptime=t.uptime))

        proxy_dict = {'proxies': proxy_records, 'http_count': http_c, 'https_count': https_c, 'http_https_count': http_https_c,
                      'socks4_count': socks4_c, 'socks5_count': socks5_c, 'socks4_socks5_count': socks4_socks5_c}
        return proxy_dict
