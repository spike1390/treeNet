# -*- coding: utf-8 -*-
import random
from models import accessControl, global_v
from flask import Blueprint, app, render_template, request, session, redirect, url_for, jsonify

index = Blueprint('index', __name__)


@index.route('/login', methods=['GET', 'POST'])
def login():

    error = None
    if not request.form['username']:
        error = 'username is null'
        return render_template('login.html', error = error)
    if not request.form['password']:
        error = 'password is null'
        return render_template('login.html', error = error)

    username = request.form['username'].encode('utf8')
    password = request.form['password'].encode('utf8')

    er = accessControl._valid_login_format(username,password)
    if er:
        return render_template('login.html', error = er)

    user = accessControl.verify(username, password)

    if user is None:
        error = 'username and password does not match'
        return render_template('login.html', error = error)
    else:
        if user.status == 0:
            error = 'User account is locked'
            return render_template('login.html', error = error)
        if user.type == 1:
            return render_template('admin.html')
        session['username'] = request.form['username']
        if not user.questions:
            return render_template('select.html',questions = global_v.fixed_questions)
        else:
              ques=user.questions
              list=[ques.sq1,ques.sq2,ques.sq3]
              #  get count from webpage , send list[index_list[count]]
              # correct answer =  verifyQues(index_list[count], session['username'])
              return render_template('validate.html', questions = list, check = 1)
        #return redirectork(url_for('index.show_network', username = username))

@index.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return render_template('login.html')

@index.route('/show_network/<username>')
def show_network(username):
    return render_template('Test.html', username = username)

@index.route('/Insert_SecureQuestions')
def Insert_SecureQuestions():
    a = request.args.get('a', 0, type=str)
    b = request.args.get('b', 0, type=str)
    c = request.args.get('c', 0, type=int)
    print c
    global_v.q_a.append(a)
    global_v.q_a.append(b)

    if c == 3:
        accessControl.createSecQues(global_v.q_a, session['username'])
        for i in global_v.q_a:
            del i

    c += 1
    print a, b
    return jsonify(result=c)

@index.route('/validate')
def validate():
    q = request.args.get('a', 0, type = str)
    index = request.args.get('c', 0, type = int)
    answer = request.args.get('b', 0, type = str)
    check = request.args.get('check', 0, type = int)
    index += 1
    re = accessControl.verifyQues(index, session['username'], answer)
    if re:
        return jsonify(result = 1, check =check)
    else:
        return jsonify(result = 0, check =check)

@index.route('/changePassword')
def change_password():
    a = request.args.get('a', 0, type = str)
    b = request.args.get('b', 0, type = str)
    username = session['username']
    print username,a,b
    re = accessControl.verify(username, a)
    msg = None
    if re:
        msg = accessControl.change_pwd(username, b)
        if msg == None:
            msg = 'success'
    else:
        msg = 'Old password wrong!'
    print msg
    return jsonify(result = msg)

@index.route('/jumpChangePwd')
def jump_change_pwd():
    return render_template('changePassword.html')

@index.route('/jumpChangeSec')
def jump_security_questions():
    return render_template('changeSecurityQuestion.html')

@index.route('/jumpValidate')
def jump_validate():
    username = session['username']
    questions = accessControl.get_security_question(username)
    list = [questions.sq1, questions.sq2, questions.sq3]
    return render_template('validate.html', check = 0, questions = list)

@index.route('/getSecurityQuestions')
def get_security_questions():
    username = session['username']
    questions = accessControl.get_security_question(username)

    return jsonify(questions = global_v.fixed_questions, question1 = questions.sq1, question2 = questions.sq2,
                   question3 = questions.sq3)

@index.route('/changeSecureQuestions')
def change_secure_questions():
    username = session['username']
    q1 = request.args.get('a', 0, type = str)
    a1 = request.args.get('b', 0, type = str)
    q2 = request.args.get('c', 0, type = str)
    a2 = request.args.get('d', 0, type = str)
    q3 = request.args.get('e', 0, type = str)
    a3 = request.args.get('f', 0, type = str)
    c1 = request.args.get('check1', 0, type = int)
    c2 = request.args.get('check2', 0, type = int)
    c3 = request.args.get('check3', 0, type = int)
    print c1, c2, c3
    re1 = 1
    re2 = 1
    re3 = 1
    if c1 != 0:
        re1 = accessControl.change_security_question(1, q1, a1, username)
    if c2 != 0:
        re2 = accessControl.change_security_question(2, q2, a2, username)
    if c3 != 0:
        re3 = accessControl.change_security_question(3, q3, a3, username)
    if re1>0 and re2>0 and re3>0:
        return jsonify(result = 1)
    else:
        return jsonify(result = 0)



@index.route('/createAccount')
def create_account():
    pass

@index.route('/deleteAccount')
def delete_account():
    pass