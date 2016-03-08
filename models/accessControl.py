# -*- coding: utf-8 -*-
import mydb
from User import User
from Question import question

# define special character dictionary
specialChar=("!","@","#","$","%","^","&","*","?")
# username='vince'
# password='asdfAAd23!@#$('

def _valid_login_format(username, password):

    if username == '':
        return "Username is null"
    else:
        if len(username)<6:
            return "Username must be at least six characters"

        else:
            # the first character of the username must be alphabeta
        # the first character of the username must be alphabeta
            if not username[0].isalpha():
                return "The first character of a username must be an alphabet"
            if not username.isalnum():
                return "Username can only have number and alphabet!"

    if password == '':
        return "Password is null"
    else:
        if len(password) < 6:
            return "Password must be at least six characters"

        else:
            for letter in password:
                if not letter.isalnum() and not letter in specialChar:
                    return "Unrecognized special characters"

    return None

def verify(username, password):
    mydb.open()
    result = mydb.query_db('select * from account WHERE username = ? and pwd = ?', [username, password], one=True)
    mydb.close_db()
    if result:
        if not result['sq_1'] == None:
            print result['sq_1']
            questions = question(result['sq_1'],result['as_1'],result['sq_2'],result['as_2'],result['sq_3'],result['as_3'])
        else:
            questions=None
        return User(result['username'], result['type'], result['status'], questions)
    else:
        return None

# store the 3 security questions and answer from user
def createSecQues(list,username):
    mydb.open()
    mydb.insert_db("""update account set sq_1= ?,as_1=? ,sq_2=?, as_2=?,sq_3=? ,as_3=? WHERE username= ?""",
    [list[0], list[1], list[2], list[3], list[4], list[5], username])
    mydb.close_db()

# Lock account, set status to '0'
def lockAccount(username):
    mydb.open()
    result = mydb.insert_db("""update account set status=0 WHERE username= ?""", (username,))
    mydb.close_db()
    return result


def verifyQues(index, username, answer):
    mydb.open()
    query = 'select as_%d from account WHERE username = ? '%index
    print query

    result = mydb.query_db(query, [username], one = True)

    mydb.close_db()
    name = 'as_%d'%index
    if result:
        return result[name] == answer
    else:
        return False

#For admin create new user. questions and answer is not included
# need parameters: username,pwd,type,status,fname,lname
def createAccount(list):
    mydb.open()
    result = _valid_login_format(list[0],list[1])
    if not result == None :
        return result
    mydb.insert_db("""insert into account(username,pwd,type,status,fname,lname)
                              values(?,?,?,?,?,?)""", [list[0], list[1], list[2], list[3], list[4], list[5]])
    mydb.close_db()
    return None


# Change user's pwd
def change_pwd(username,pwd):
    mydb.open()
    result=_valid_login_format(username,pwd)
    if not result==None:
        return result
    mydb.insert_db("""update account set pwd=? WHERE username= ?""", [pwd, username])
    mydb.close_db()
    return None

def get_security_question(username):
    mydb.open()
    result = mydb.query_db('select * from account WHERE username = ? ', [username], one=True)
    mydb.close_db()
    if result:
        questions = question(result['sq_1'],result['as_1'],result['sq_2'],result['as_2'],result['sq_3'],result['as_3'])
        return questions
    else:
        return None

def change_security_question(index, q, a, username):
    if len(a) == 0:
        return -1
    mydb.open()
    query = 'update account set sq_%d= ?,as_%d=? WHERE username = ?' % (index, index)
    print query
    mydb.insert_db(query, [q, a, username])
    mydb.close_db()
    return 1
# createAccount(['spike1123','2cs744',0,1,'Zhishang','Wang'])

#addAccount(['spike1390','2cs744',0,1])

#print verifyQues(3,'spikewang','asdfasdfs')