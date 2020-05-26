from recordclass import RecordClass


class Isp(RecordClass):
    isp_id: int
    isp_name: str

    def __hash__(self):
        return hash((self.isp_id, self.isp_name))

    def __eq__(self, other):
        if isinstance(other, Isp):
            return self.isp_id, self.isp_name == other.isp_id, other.isp_name
        else:
            return False
