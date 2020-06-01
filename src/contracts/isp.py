from recordclass import RecordClass


class Isp(RecordClass):
    id: int
    name: str

    def __hash__(self):
        return hash((self.id, self.name))

    def __eq__(self, other):
        if isinstance(other, Isp):
            return self.id, self.name == other.id, other.name
        else:
            return False
