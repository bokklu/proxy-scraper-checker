from aenum import Enum


class ProxyType(Enum):
    HTTP = 1
    HTTPS = 2
    HTTP_HTTPS = 3
    SOCKS4 = 4
    SOCKS5 = 5
    SOCKS4_SOCKS5 = 6


class Response(Enum):
    SUCCESS = 1
    ERROR = 2
    TIMEOUT = 3
    OTHER = 4
    ERROR_OTHER = 5


class ProxyAccessType(Enum):
    TRANSPARENT = 1
    ANONYMOUS = 2
    ELITE = 3

    @classmethod
    def _missing_name_(cls, name):
        for member in cls:
            if member.name.lower() == name.lower():
                return member


class Provider(Enum):
    PLDOWN = 1
    PROXYSCRAPE = 2
