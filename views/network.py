# -*- coding: utf-8 -*-
import json
from models import netModel
from flask import Blueprint, app, render_template, request, session,jsonify

network = Blueprint('network', __name__)

@network.route('/whole_network')
def return_whole_network():
    ps = netModel.return_net()
    a = 96
    dis_string = []
    for p in ps:
        tmp_str = ''
        print p.id
        if len(p.nodes) == 1:
            tmp_str = '%s%s'% (chr(a+p.id),p.nodes[0].id)
        else:
            length = len(p.nodes)
            for i in range(0, length):
                for j in range(i,length):
                    index1 = p.nodes[i].index
                    index2 = p.nodes[j].index
                    if index2 == 2*index1:
                        tmp_str = tmp_str + '%s%s--%s%s;'%(chr(a+p.id),p.nodes[i].id,chr(a+p.id), p.nodes[j].id)
                    if index2 == 2*index1+1:
                        tmp_str = tmp_str + '%s%s--%s%s;'%(chr(a+p.id),p.nodes[i].id, chr(a+p.id),p.nodes[j].id)

        if len(tmp_str) != 0 and tmp_str[len(tmp_str)-1] == ';':
            tmp_str = tmp_str[:-1]
        dis_string.append(tmp_str)
    return jsonify(result=dis_string)

@network.route('/add_node')
def add_node(pid,index):
    netModel.add_note(pid,index)
    return