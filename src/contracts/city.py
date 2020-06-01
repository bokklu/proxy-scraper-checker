from recordclass import RecordClass


class City(RecordClass):
    proxy_address: str
    latitude: float
    longitude: float
    city_name: str
    sub_division1: str
    sub_division1_code: str
    sub_division2: str
    sub_division2_code: str
    postal_code: str
    accuracy_radius: int
    timezone: str

    def __hash__(self):
        return hash(self.proxy_address)

    def __eq__(self, other):
        if isinstance(other, City):
            return self.proxy_address == other.proxy_address
        else:
            return False
