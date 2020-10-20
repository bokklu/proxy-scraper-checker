import logging
from contracts.enums import Response, ProxyType, Provider
from contracts.proxy import Proxy


class ProxyHelper:

    @staticmethod
    def create_and_log_proxy_stats(proxies, task_results, provider_id):
        proxy_records = set()
        http_c = http_ssl_c = socks4_c = socks5_c = 0

        for t in task_results:

            if t.result_type is Response.SUCCESS:
                if t.type_id is ProxyType.HTTP.value:
                    if t.ssl is False:
                        http_c += 1
                    else:
                        http_ssl_c += 1
                elif t.type_id is ProxyType.SOCKS4.value:
                        socks4_c += 1
                elif t.type_id is ProxyType.SOCKS5.value:
                        socks5_c += 1

                proxy_records.add(Proxy(address=t.address, port=t.port, country_code=t.country_code,
                                        provider_id=provider_id,
                                        access_type_id=t.access_type_id, type_id=t.type_id, speed=t.speed,
                                        uptime=t.uptime))

        logging.info(f'Successful: {len(proxy_records)}/{len(task_results)}\n'
                     f'HTTP => [{http_c}/{len(proxies[0])}]\n'
                     f'HTTP SSL => [{http_ssl_c}/{len(proxies[1])}]\n'
                     f'SOCKS4 => [{socks4_c}/{len(proxies[2])}]\n'
                     f'SOCKS5 => [{socks5_c}/{len(proxies[3])}]')

        return proxy_records
