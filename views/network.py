# -*- coding: utf-8 -*-
import json
from operator import methodcaller
from models import netModel,global_v
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
    print pid, index
    nid = netModel.add_node(pid, index)
    return jsonify(result1 = nid)

@network.route('/addPattern')
def add_pattern():
    a = request.args.get('a',0,type = str)
    b = request.args.get('b',0,type = str)
    ps = json.loads(a)
    node = json.loads(b)
    print ps, node
    re = netModel.add_pattern(ps)

    return jsonify(result1= re[0], result2 = re[1])

@network.route('/deleteNode')
def delete_node():
    a = request.args.get('a', 0, type = str)
    nodes = json.loads(a)
    netModel.delete_node(nodes)
    print nodes
    return jsonify()

@network.route('/deletePattern')
def delete_pattern():
    a = request.args.get('a', 0, type = str)
    nodeId = json.loads(a)
    print nodeId
    nid = nodeId['pid']
    netModel.delete_pattern(nid)

    return jsonify()

@network.route('/activeNode')
def active_node():
    a = request.args.get('a', 0, type = str)
    nid = int(a)
    netModel.change_node_status(nid, 1)
    return jsonify()