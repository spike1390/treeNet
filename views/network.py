# -*- coding: utf-8 -*-
import json
from operator import methodcaller
from models import netModel,global_v,SendMessage
from flask import Blueprint, app, render_template, request, session, jsonify

network = Blueprint('network', __name__)



@network.route('/whole_network')
def return_whole_network():
    ran = global_v.ran
    net = netModel.return_json()

    return jsonify(result1=net, ranNum = ran)

@network.route('/addNode')
def add_node():
    a = request.args.get('a',0,type = str)
    node = json.loads(a)
    pid = node['pid']
    index = node['index']
    nid = netModel.add_node(pid, index)
    return jsonify(result1 = nid)

@network.route('/addPattern')
def add_pattern():
    a = request.args.get('a',0,type = str)
    b = request.args.get('b',0,type = int)
    ps = json.loads(a)
    re = netModel.add_pattern(ps,b)
    return jsonify(result1= re[0], result2 = re[1])


@network.route('/addDomain')
def add_domain():
    a = request.args.get('a',0,type = str)
    ds = json.loads(a)
    re = netModel.add_domain(ds)
    return jsonify(result1= re[1], result2 = re[2],result3 =re[0], result4=re[3])


@network.route('/deleteNode')
def delete_node():
    a = request.args.get('a', 0, type = str)
    nodes = json.loads(a)
    netModel.delete_node(nodes)
    return jsonify()

@network.route('/deletePattern')
def delete_pattern():
    a = request.args.get('a', 0, type = str)
    nodeId = json.loads(a)
    print nodeId
    did = nodeId['did']
    pid = nodeId['pid']
    if did != -1:
        netModel.delete_domain(pid, did)
    else:
        netModel.delete_pattern(pid)
    return jsonify()

@network.route('/activeNode')
def active_node():
    nid = int(request.args.get('a', 0, type = str))
    netModel.change_node_status(nid, 1)
    msg_list= SendMessage.get_resend_msg_list(nid)
    return jsonify(result = msg_list)

@network.route('/addConnection')
def add_connection():
    a = request.args.get('a', 0, type = str)
    b = request.args.get('b', 0, type = str)
    nid1 = int(a)
    nid2 = int(b)
    netModel.add_connection(nid1,nid2)
    return jsonify()

@network.route('/deleteConnection')
def delete_connection():
    a = request.args.get('a', 0, type = str)
    b = request.args.get('b', 0, type = str)
    nid1 = int(a)
    nid2 = int(b)
    netModel.delete_connection(nid1,nid2)
    return jsonify()