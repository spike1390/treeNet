import sqlite3,json
from operator import methodcaller
from Node import edge,Node,pattern,domain
import path

def query_db(query, args=(), one=False):
    db = sqlite3.connect(path.db_path)

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

def one_pattern_edge(pid):
    edges = []
    results = query_db('SELECT * FROM edge WHERE _from = ?', [pid])
    for e in results:
        to_pid = e['_to']
        result = query_db('SELECT * FROM pattern WHERE pid = ?', [to_pid], one = True)
        if result['isDomain'] == 0:
            edges.append(to_pid)
    return edges

def one_domain_edge(did):
    edges = []
    domain_pattern = query_db('SELECT * FROM pattern WHERE did = ? and isDomain = 1', [did], one = True)
    pid = domain_pattern['pid']
    results = query_db('SELECT * FROM edge WHERE _from = ?', [pid])
    for e in results:
        to_pid = e['_to']
        result = query_db('SELECT * FROM pattern WHERE pid = ?', [to_pid], one = True)
        if result['isDomain'] == 1:
            edges.append(result['did'])
    return edges
# def get_nodes_edges(nodes):
#     edges = []
#     for n1 in nodes:
#         n1_index = n1.index
#         if n1_index in [0, 1, 2]:
#             for n2 in nodes:
#                 if n2.index in [n1_index*2+1, n1_index*2+2] and n1.pid == n2.pid:
#                     source = n1.nid
#                     target = n2.nid
#                     tmp_edge = edge(source, target)
#                     edges.append(tmp_edge)
#     return edges


def return_json():
    nodes = []
    nodes_results = query_db('SELECT * FROM node ')
    # print "the nodes has %s node" % len(nodes_results)
    for n in nodes_results:
        tmp_node = Node(n['nid'], n['pid'], n['node_index'], n['active'])
        nodes.append(tmp_node)

    # print json.dumps(nodes, default = methodcaller("json"))
    ps = return_ps(nodes)
    # print json.dumps(get_nodes_edges(nodes)+return_p_edges(), default = methodcaller("json"))
    # print json.dumps(return_ps(nodes), default = methodcaller("json"))
    return json.dumps(return_ds(ps), default = methodcaller("json"))


def return_ps(ns):
    results = query_db('SELECT * FROM pattern WHERE isDomain = 0')
    ps = []
    for r in results:
        tmp_p = pattern(r['pid'], r['did'])
        tmp_p.outEdges = one_pattern_edge(r['pid'])
        ps.append(tmp_p)

    for p in ps:
        for n in ns:
            if n.pid == p.id:
                p.nodes.append(n)
    return ps

def return_ds(ps):
    results = query_db('SELECT * FROM domain ')
    ds = []
    for r in results:
        tmp_d = domain(r['did'])
        tmp_d.domain_edges = one_domain_edge(r['did'])
        domain_pattern = query_db('SELECT * FROM pattern WHERE did = ? and isDomain = 1', [r['did']], one = True)
        node = query_db('SELECT * FROM node WHERE pid = ? ', [domain_pattern['pid']], one = True)
        tmp_node = Node(node['nid'], -1, -1, node['active'])
        tmp_d.domain_node = tmp_node
        ds.append(tmp_d)


    for d in ds:
        for p in ps:
            if p.did == d.did:
                d.patterns.append(p)
    return ds



