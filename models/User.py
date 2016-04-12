class JSONEncodable(object):
    def json(self):
        return vars(self)

class User(JSONEncodable):

    def __init__(self, name, u_type, status=None, questions = None,fname=None,lname=None,pwd=None):
        self.questions = []
        self.name = name
        self.type = u_type
        self.status = status
        self.fname=fname;
        self.lname=lname;
        self.pwd=pwd;
        self.questions = questions
