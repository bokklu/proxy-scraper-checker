from contracts.enums import Response
from dataclasses import dataclass


@dataclass
class Statistics:
    address: str = None
    port: int = None
    country_code: str = None
    access_type_id: int = None
    type_id: int = None
    speed: int = None
    uptime: int = None
    result_type: Response = Response.TIMEOUT
