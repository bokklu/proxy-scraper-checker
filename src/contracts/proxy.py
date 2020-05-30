from recordclass import RecordClass


class Proxy(RecordClass):
    address: str
    port: int
    provider_id: int
    country_code: str = None
    access_type_id: int = None
    type_id: int = None
    isp_id: int = None
    speed: int = None
    uptime: int = None

    def __hash__(self):
        return hash((self.address, self.port, self.type_id, self.access_type_id))

    def __eq__(self, other):
        if isinstance(other, Proxy):
            return self.address, self.port, self.type_id == other.address, other.port, other.type_id
        else:
            return False
