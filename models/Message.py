class message:

    def __init__(self, _from=None, _to=None, msg=None, path=None):

        self._from =_from
        self._to = _to
        self.path=transform_list_toStr(path)
        self.msg=msg

def transform_list_toStr(path_list):
    if path_list==None:
     return None
    string=''
    for i in path_list:
        string+=(str(i)+' ').encode('utf-8')
        return string[0:len(string)-1]

    def __repr__(self):
        return "from " + self._from + " to "+ self._to +" msg " +self.msg