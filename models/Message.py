
class JSONEncodable(object):
    def json(self):
        return vars(self)

class message(JSONEncodable):
    #  path is a list of integer
    def __init__(self, _from=None, _to=None, msg=None, path=None ,createdAt=None, sender=None, msgId=None, blockedAt=None):

        self._from = _from
        self._to = _to
        self.path = path
        self.sender=sender
        self.createdAt = createdAt
        self.blockedAt=blockedAt
        self.msgId=msgId
        # transform_list_toStr(path)
        self.msg=msg



    def __repr__(self):
        return   str(self._from) + "to"+ str(self._to) +" msgid " +str(self.msgId)+" sender"+ str(self.sender)+" msg"+ str(self.msg)

    def __eq__(self, other):
        return hash(self)==hash(other)
