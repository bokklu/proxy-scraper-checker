from dataclasses import dataclass


@dataclass
class ScrapeInfo:
    proxy: str
    country_code: str = None
    access_type_id: int = None

    def __hash__(self):
        return hash(self.proxy)

    def __eq__(self, other):
        if isinstance(other, ScrapeInfo):
            return self.proxy == other.proxy
        else:
            return False
