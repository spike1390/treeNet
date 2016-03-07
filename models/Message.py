
class JSONEncodable(object):
    def json(self):
        return vars(self)

class message(JSONEncodable):
    #  path is a list of integer
    def __init__(self, _from=None, _to=None, msg=None, path=None ,createdAt=None):

        self._from = _from
        self._to = _to
        self.path = path
        self.createdAt = createdAt
        # transform_list_toStr(path)
        self.msg=msg



    def __repr__(self):
        return "from " + self._from + " to "+ self._to +" msg " +self.msg