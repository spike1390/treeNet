import json
from flask import Blueprint, app, render_template, request, session, redirect, url_for, jsonify
from models import SendMessage, PathFinder,global_v
message = Blueprint('message', __name__)

@message.route('/wholeMessages')
def whole_messages():
    ms = SendMessage.view_all_message()
    fms = SendMessage.view_failed_message()
    return jsonify(result1 = ms,result2 = fms)

@message.route('/sendMessage')
def send_message():
    a = request.args.get('a',0,type = str)
    b = request.args.get('b',0,type = str)
    c = request.args.get('c',0,type = str)
    d = request.args.get('d',0,type = str)
    nid1 = int(a)
    nid2 = int(b)
    msg = c
    msgId=int(d)
    if msgId==-1:
        global_v.msgId += 1
        msgId=global_v.msgId
    path = PathFinder.send_msg(nid1, nid2, msg, msgId)
    path = json.dumps(path)

    return jsonify(result = path,count=msgId)

@message.route('/verifyNode')
def verify_node():

    preId = request.args.get('a',0,type = str)
    curId = request.args.get('b',0,type = str)

    msgId = request.args.get('c',0,type = int)
    # re = SendMessage.check_node_in_path(a, b)
    if not SendMessage.check_node_in_path(int(preId), int(curId), int(msgId)):
        r = 0
    else:
        r = 1

    return jsonify(result = r)



