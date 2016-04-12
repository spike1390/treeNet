# -*- coding: utf-8 -*-
import mydb, json
from User import User
from Question import question
from operator import methodcaller

# define special character dictionary
specialChar=("!","@","#","$","%","^","&","*","?")
# username='vince'
# password='asdfAAd23!@#$('

def _valid_login_format(username, password):

    if username == '':
        return ["Username is null",2]
    else:
        if len(username)<6:
            return ["Username must be at least six characters",2]

        else:
            # the first character of the username must be alphabeta
        # the first character of the username must be alphabeta
            if not username[0].isalpha():
                return ["The first character of a username must be an alphabet",2]
            if not username.isalnum():
                return ["Username can only have number and alphabet!",2]

    if password == '':
        return ["Password is null",3]
    else:
        if len(password) < 6:
            return ["Password must be at least six characters",3]

        else:
            for letter in password:
                if not letter.isalnum() and not letter in specialChar:
                    return ["Unrecognized special characters",3]

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

# return a user list .user object contains: username, type, fname, lname , pwd
def get_all_users():
    mydb.open()
    result = mydb.query_db('select * from account WHERE type = 0',[],one=False)
    mydb.close_db()
    userList=[]
    for user in result:
       dict = {'name':user['username'],'fname':user['fname'],'lname':user['lname']}
       userList.append(dict)
    return userList

#For admin create new user. questions and answer is not included
# input list should be in format of: [ username,pwd,type,status,fname,lname]
def createAccount(list):
    mydb.open()
    if len(list[4])==0:
        return ["First name can't be null", 0]
    if len(list[5])==0:
        return ["Last name can't be null",1]
    result = _valid_login_format(list[0],list[1])
    # if error happend return error message
    if not result == None :
        return result
    if not check_username(list[0]):
        return ["Username has already existed",2]
    mydb.insert_db("""insert into account(username,pwd,type,status,fname,lname)
                              values(?,?,?,?,?,?)""", [list[0], list[1], list[2], list[3], list[4], list[5]])
    mydb.close_db()
    return None


# for admin to delete a user from database
def delete_user(username):
     mydb.open()
     mydb.delete_db('delete from account where username = ? ',[username])
     mydb.close_db()

def check_username(username):
    mydb.open()
    result = mydb.query_db('select * from account WHERE username = ?', [username], one=True)
    if result==None:
        return True
    else:
        return False


# createAccount(['spike1123','2cs744',0,1,'Zhishang','Wang'])

#addAccount(['spike1390','2cs744',0,1])

#print verifyQues(3,'spikewang','asdfasdfs')

