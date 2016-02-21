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
            questions=question(result['sq_1'],result['as_1'],result['sq_2'],result['as_2'],result['sq_3'],result['as_3'])
        else:
            questions=None
        return User(result['username'], result['type'], result['status'], questions)
    else:
        return None

# store the 3 security questions and answer from user
def createSecQues(list,username):
    mydb.insert_db("""update account set sq_1= ?,as_1=? ,sq_2=?, as_2=?,sq_3=? ,as_3=? WHERE username= ?""",
    [list[0], list[1], list[2], list[3], list[4], list[5], username])

# Lock account, set status to '0'
def lockAccount(username):
    result = mydb.insert_db("""update account set status=0 WHERE username= ?""", (username,))
    return result



#For admin create new user. questions and answer is not included
def addAccount(list):
      result = mydb.insert_db("""insert into account(username,pwd,type,status)
                              values(?,?,?,?)""",[list[0],list[1],list[2],list[3]] )

print verify('spike1390','2cs744').questions