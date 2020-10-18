from contracts.enums import Response


class Statistics:

    def __init__(self, address=None, port=None, country_code=None, access_type_id=None, type_id=None, ssl=None,
                 get=None, post=None, speed=None, uptime=None, result_type=Response.TIMEOUT):
        self.address = address
        self.port = port
        self.country_code = country_code
        self.access_type_id = access_type_id
        self.type_id = type_id
        self.ssl = ssl
        self.get = get
        self.post = post
        self.speed = speed
        self.uptime = uptime
        self.result_type = result_type
