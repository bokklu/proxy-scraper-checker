from contracts.isp import Isp
from contracts.city import City
from config import geo_db
from geoip2.database import Reader
from geoip2.errors import AddressNotFoundError
from dataclasses import dataclass


@dataclass
class GeoRepo:
    _city_db: Reader = Reader(geo_db['city_db'])
    _asn_db: Reader = Reader(geo_db['asn_db'])
    get_country: bool = False

    def __city_resolve(self, proxy):
        try:
            city_record = self._city_db.city(proxy.address)

            if self.get_country: proxy.country_code = city_record.country.iso_code

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
                            city_name=city_record.city.name, sub_division1=sub_division1, sub_division1_code=sub_division1_code,
                            sub_division2=sub_division2, sub_division2_code=sub_division2_code,  postal_code=city_record.postal.code,
                            accuracy_radius=city_record.location.accuracy_radius, timezone=city_record.location.time_zone)

        except AddressNotFoundError:
            print(f'{proxy.address} not found in CITY mmdb...')
            return None

    def __isp_resolve(self, proxy):
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

    def geo_resolve(self, proxies):
        isps, cities = set(), set()

        for proxy in proxies:

            isp_result = self.__isp_resolve(proxy)
            if isp_result is not None: isps.add(isp_result)

            city_result = self.__city_resolve(proxy)
            if city_result is not None: cities.add(city_result)

        return isps, cities
