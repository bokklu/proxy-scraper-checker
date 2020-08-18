from contracts.enums import Response


class Statistics:
    address: str = None
    port: int = None
    country_code: str = None
    access_type_id: int = None
    type_id: int = None
    speed: int = None
    uptime: int = None
    result_type: Response = Response.TIMEOUT

    def __init__(self, address=None, port=None, country_code=None, access_type_id=None, type_id=None, speed=None, uptime=None, result_type=Response.TIMEOUT):
        self.address = address
        self.port = port
        self.country_code = country_code
        self.access_type_id = access_type_id
        self.type_id = type_id
        self.speed = speed
        self.uptime = uptime
        self.result_type = result_type
