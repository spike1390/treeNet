class User:

    def __init__(self, name, u_type, status, questions = None):
        self.questions = []
        self.name = name
        self.type = u_type
        self.status = status

        self.questions = questions
