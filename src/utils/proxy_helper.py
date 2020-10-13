from contracts.enums import Response, ProxyType, Provider
from contracts.proxy import Proxy


class ProxyHelper:

    @staticmethod
    def create_and_get_proxy_stats(task_results, provider_id):
        proxy_records = set()
        http_c = https_c = socks4_c = socks5_c = 0

        f = open("incorrect-http.txt", "w")

        for t in task_results:

            if t.result_type is Response.SUCCESS:
                if t.type_id is ProxyType.HTTP.value: http_c += 1
                elif t.type_id is ProxyType.HTTPS.value: https_c += 1
                elif t.type_id is ProxyType.SOCKS4.value: socks4_c += 1
                elif t.type_id is ProxyType.SOCKS5.value: socks5_c += 1

                proxy_records.add(Proxy(address=t.address, port=t.port, country_code=t.country_code,
                                        provider_id=provider_id,
                                        access_type_id=t.access_type_id, type_id=t.type_id, speed=t.speed,
                                        uptime=t.uptime))
            elif t.type_id is ProxyType.HTTP.value:
                f.write(f'{t.address}:{t.port}\n')

        f.close()

        return {'proxies': proxy_records, 'http_count': http_c, 'https_count': https_c,
                'socks4_count': socks4_c, 'socks5_count': socks5_c}
