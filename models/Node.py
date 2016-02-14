
class JSONEncodable(object):
    def json(self):
        return vars(self)

class Node(JSONEncodable):

    def __init__(self, nid, pid, index):
        self.id = nid
        self.pid = pid
        self.index = index

    def __cmp__(self, other):
        if hasattr(other, 'index'):
            return self.index.__cmp__(other.index)
