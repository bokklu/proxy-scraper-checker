from aenum import Enum


class ProxyType(Enum):
    HTTP = 1
    HTTPS = 2
    SOCKS4 = 3
    SOCKS5 = 4


class Response(Enum):
    SUCCESS = 1
    ERROR = 2
    TIMEOUT = 3
    OTHER = 4


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
