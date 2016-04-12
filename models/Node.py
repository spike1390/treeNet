
class JSONEncodable(object):
    def json(self):
        return vars(self)



class Node(JSONEncodable):

    def __init__(self, nid, pid, index, active = None):
        self.nid = nid
        self.pid = pid
        self.index = index
        self.active = active




class edge(JSONEncodable):
    def __init__(self, source, target):
        self.id = str(source) + '-' + str(target)
        self.source = source
        self.target = target

class pattern(JSONEncodable):

    def __init__(self, id, did):
        self.id = id
        self.nodes = []
        self.did = did
        self.outEdges = []

class domain(JSONEncodable):

    def __init__(self, id):
        self.did = id
        self.patterns = []
        self.domain_edges = []

