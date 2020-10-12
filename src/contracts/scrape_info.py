class ScrapeInfo:

    def __init__(self, proxy, country_code=None, access_type_id=None):
        self.proxy = proxy
        self.country_code = country_code
        self.access_type_id = access_type_id

    def __hash__(self):
        return hash((self.proxy, self.country_code, self.access_type_id))

    def __eq__(self, other):
        if isinstance(other, ScrapeInfo):
            return self.proxy == other.proxy
        else:
            return False
