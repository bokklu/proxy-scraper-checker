from contracts.isp import Isp
from contracts.city import City
from geoip2.database import Reader
from geoip2.errors import AddressNotFoundError


class GeoRepo:

    def __init__(self, config):
        self._city_db = Reader(config['geo_db']['city_db'])
        self._asn_db = Reader(config['geo_db']['asn_db'])

    def _city_resolve(self, get_country, proxy):
        try:
            city_record = self._city_db.city(proxy.address)

            if get_country: proxy.country_code = city_record.country.iso_code

            sub_division1 = sub_division1_code = sub_division2 = sub_division2_code = None
            subdivision_count = len(city_record.subdivisions)

            if subdivision_count != 0:
                if subdivision_count == 1:
                    sub_division1 = city_record.subdivisions[0].name
                    sub_division1_code = city_record.subdivisions[0].iso_code
                elif subdivision_count == 2:
                    sub_division2 = city_record.subdivisions[1].name
                    sub_division2_code = city_record.subdivisions[1].iso_code

            return City(proxy_address=proxy.address, latitude=city_record.location.latitude, longitude=city_record.location.longitude,
                            name=city_record.city.name, sub_division1=sub_division1, sub_division1_code=sub_division1_code,
                            sub_division2=sub_division2, sub_division2_code=sub_division2_code,  postal_code=city_record.postal.code,
                            accuracy_radius=city_record.location.accuracy_radius, timezone=city_record.location.time_zone)

        except AddressNotFoundError:
            print(f'{proxy.address} not found in CITY mmdb...')
            return None

    def _isp_resolve(self, proxy):
        try:
            isp_record = self._asn_db.asn(proxy.address)
            isn_number = isp_record.autonomous_system_number
            proxy.isp_id = isn_number

            if isn_number is not None:
                return Isp(id=isp_record.autonomous_system_number, name=isp_record.autonomous_system_organization)
            else:
                return None
        except AddressNotFoundError:
            print(f'{proxy.address} not found in ASN mmdb...')
            return None

    def geo_resolve(self, proxies, get_country):
        isps, cities, missing_proxies = set(), set(), set()

        for proxy in proxies:

            isp_result = self._isp_resolve(proxy)
            isps.add(isp_result) if isp_result is not None else missing_proxies.add(proxy)

            city_result = self._city_resolve(get_country, proxy)
            cities.add(city_result) if city_result is not None else missing_proxies.add(proxy)

        geo_filtered_proxies = list(proxies ^ missing_proxies)

        return isps, cities, geo_filtered_proxies
