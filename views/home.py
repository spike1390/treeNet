# -*- coding: utf-8 -*-

from models import accessControl
from flask import Blueprint, app, render_template, request, session, redirect, url_for

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
        #session['username'] = request.form['username']
        error = 'success'
        return render_template('Test.html')

@index.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return