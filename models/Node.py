
class JSONEncodable(object):
    def json(self):
        return vars(self)



class Node(JSONEncodable):

    def __init__(self, nid, pid, index, active = None, x=None , y=None ):
        self.color = 'rgb(255,168,7)'
        self.label = str(nid)
        self.nid = nid
        self.pid = pid
        self.index = index
        self.active = active
        if index == 1:
            self.shape = 'diamond'
        else:
            self.shape = 'ellipse'
        self.x = x
        self.y = y



class edge(JSONEncodable):
    def __init__(self, source, target):
        self.id = str(source) + '-' + str(target)
        self.source = source
        self.target = target

class pattern(JSONEncodable):

    def __init__(self, id):
        self.id = id
        self.nodes = []
        self.outEdges = []
