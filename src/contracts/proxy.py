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
        return hash((self.address, self.port))

    def __eq__(self, other):
        if isinstance(other, Proxy):
            return self.address, self.port == other.address, other.port
        else:
            return False
