import sqlite3,json
from operator import methodcaller
from Node import edge,Node,pattern
db_path = '/Users/wangzhishang/PycharmProjects/run/test.db'

def query_db(query, args=(), one=False):
    db = sqlite3.connect(db_path)

    cur = db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
                for idx, value in enumerate(row)) for row in cur.fetchall()]
    db.close()
    return (rv[0] if rv else None) if one else rv

def return_p_edges():
    edges = []
    results = query_db('SELECT * FROM edge ')
    for e in results:
        source = e['_from']
        target = e['_to']
        tmp_edge = edge(source, target)
        edges.append(tmp_edge)
    return edges

def get_nodes_edges(nodes):
    edges = []
    for n1 in nodes:
        n1_index = n1.index
        if n1_index in [0, 1, 2]:
            for n2 in nodes:
                if n2.index in [n1_index*2+1, n1_index*2+2] and n1.pid == n2.pid:
                    source = n1.nid
                    target = n2.nid
                    tmp_edge = edge(source, target)
                    edges.append(tmp_edge)
    return edges


def return_json():
    nodes = []
    nodes_results = query_db('SELECT * FROM node ')
    # print "the nodes has %s node" % len(nodes_results)
    for n in nodes_results:
        tmp_node = Node(n['nid'], n['pid'], n['node_index'], n['active'], n['x'], n['y'])
        nodes.append(tmp_node)

    print json.dumps(nodes, default = methodcaller("json"))
    print json.dumps(get_nodes_edges(nodes)+return_p_edges(), default = methodcaller("json"))
    print json.dumps(return_ps(nodes), default = methodcaller("json"))


def return_ps(ns):

    re = []
    results = query_db('SELECT * FROM pattern ')
    ps = []
    for p in results:
        ps.append(p['pid'])

    for p in ps:
        tmp_p = pattern(p)
        for n in ns:
            if n.pid == p:
                tmp_p.nodes.append(n)
        re.append(tmp_p)



    return re


return_json()


