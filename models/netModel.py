import mydb, json
from Node import Node,edge,pattern

from operator import methodcaller

def return_p_edges():
    edges = []
    mydb.open()
    results = mydb.query_db('SELECT * FROM edge ')
    for e in results:
        source = e['_from']
        target = e['_to']
        tmp_edge = edge(source, target)
        edges.append(tmp_edge)
    mydb.close_db()
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
    mydb.open()
    nodes_results = mydb.query_db('SELECT * FROM node ')
    # print "the nodes has %s node" % len(nodes_results)
    for n in nodes_results:
        tmp_node = Node(n['nid'], n['pid'], n['node_index'], n['active'], n['x'], n['y'])
        nodes.append(tmp_node)
    mydb.close_db()
    # print json.dumps(nodes, default = methodcaller("json"))
    # print json.dumps(get_nodes_edges(nodes)+return_p_edges(), default = methodcaller("json"))
    return json.dumps(return_ps(nodes), default = methodcaller("json"))

def one_pattern_edge(pid):
    edges = []
    mydb.open()
    results = mydb.query_db('SELECT * FROM edge WHERE _from = ?', [pid])
    for e in results:
        edges.append(e['_to'])
    mydb.close_db()
    return edges

def return_ps(ns):
    mydb.open()
    re = []
    results = mydb.query_db('SELECT * FROM pattern ')
    ps = []
    for p in results:
        ps.append(p['pid'])

    for p in ps:
        tmp_p = pattern(p)
        for n in ns:
            if n.pid == p:
                tmp_p.nodes.append(n)
                tmp_p.outEdges = one_pattern_edge(p)
        re.append(tmp_p)


    mydb.close_db()
    return re

def add_pattern(ps):
    mydb.open()
    pid = mydb.insert_db('INSERT INTO pattern (creator) VALUES (?)',['spikewang'])
    print pid
    nid = mydb.insert_db('INSERT INTO node (pid,node_index,active) VALUES (?,1,1)', [pid])
    for p in ps:
        mydb.insert_db('INSERT INTO  edge(_from, _to) VALUES (?,?)',[pid,p])
    mydb.close_db()
    return (pid, nid)

def add_node(pid,index):
    mydb.open()
    results = mydb.query_db('SELECT * FROM node WHERE pid = ? and node_index = ?', [pid, index/2] )
    if len(results)!=0:
        nid = mydb.insert_db('INSERT INTO node (pid,node_index,active) VALUES (?,?,1)',[pid,index])
        mydb.close_db()
        return nid
    else:
        return -1

def delete_node(nids):
    mydb.open()
    for n in nids:
        mydb.delete_db('delete from node where nid = ?',[n])
    mydb.close_db()



def delete_pattern(pattern_id):
    mydb.open()
    nodes = mydb.query_db('SELECT * FROM node WHERE pid = ?',[pattern_id])
    if len(nodes) > 1:
        return False
    prohibited_node = []
    results = mydb.query_db('SELECT * FROM pattern')
    for p in results:
        pid = p['pid']
        re1 = mydb.query_db('SELECT * FROM edge WHERE _from = ?',[pid])
        re2 = mydb.query_db('SELECT * FROM edge WHERE _to = ?',[pid])
        if len(re1)+len(re2) == 1:
            if len(re1) == 1:
                pro = re1[0]['_to']
            else:
                pro = re2[0]['_from']
            prohibited_node.append(pro)
    print prohibited_node
    if pid in prohibited_node:
        mydb.close_db()
        return False
    else:
        mydb.delete_db('delete from edge where _from = ? or _to = ?',[pattern_id, pattern_id])
        mydb.delete_db('delete from pattern where pid=?', [pattern_id])
        mydb.delete_db('delete from node where pid=? and node_index = 1', [pattern_id])
        mydb.close_db()
        return True



# print return_json()
#print add_node(4,3)
# delete_node([7,8,9])
# print add_pattern([1,2])[1]
# add_node(4,3)
# print delete_pattern(4)

