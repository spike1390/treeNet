
class JSONEncodable(object):
    def json(self):
        return vars(self)


class Pattern(JSONEncodable):

    def __init__(self, pid, connector):
        self.id = pid
        self.connector = connector
        self.nodes = []





