import json
from flask import Blueprint, app, render_template, request, session, redirect, url_for, jsonify
from models import SendMessage, PathFinder
message = Blueprint('message', __name__)

@message.route('/wholeMessages')
def whole_messages():
    print 'dasdas'
    ms = SendMessage.view_all_message()
    print ms
    return jsonify(result1 = ms)

@message.route('/sendMessage')
def send_message():
    a = request.args.get('a',0,type = str)
    b = request.args.get('b',0,type = str)
    c = request.args.get('c',0,type = str)
    print a,b,c
    nid1 = int(a)
    nid2 = int(b)
    msg = c
    path = PathFinder.send_msg(nid1, nid2, msg)
    path = json.dumps(path)
    print path
    return jsonify(result = path)

@message.route('/verifyNode')
def verify_node():

    a = request.args.get('a',0,type = str)
    b = request.args.get('b',0,type = str)

    # re = SendMessage.check_node_in_path(a, b)
    if not SendMessage.check_node_in_path(int(a), int(b)):
        r = 0
    else:
        r = 1

    return jsonify(result = r)



