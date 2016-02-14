# -*- coding: utf-8 -*-
import mydb
from User import User

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
    return User(result['username'], result['type'], result['status']) if result else None



