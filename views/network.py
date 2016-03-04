# -*- coding: utf-8 -*-
import json
from operator import methodcaller
from models import netModel
from flask import Blueprint, app, render_template, request, session, jsonify

network = Blueprint('network', __name__)



@network.route('/whole_network')
def return_whole_network():

    net = netModel.return_json()
    print net
    return jsonify(result1=net)

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