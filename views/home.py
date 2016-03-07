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
              return render_template('validate.html', questions = list)
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
    index += 1
    re = accessControl.verifyQues(index, session['username'], answer)
    if re:
        return jsonify(result = 1)
    else:
        return jsonify(result = 0)

@index.route('/changePassword')
def change_password():
    #accessControl.change_pwd()
    pass

@index.route('/createAccount')
def create_account():
    pass

@index.route('/deleteAccount')
def delete_account():
    pass