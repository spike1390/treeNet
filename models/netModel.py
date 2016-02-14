import mydb
from Node import Node
from Pattern import Pattern

def add_note(pid, index):
    mydb.open()
    nid = mydb.insert_db('INSERT INTO node (pid, node_index) VALUES (?,?)',
                [pid, index])
    mydb.close_db()
    return nid

def add_pattern(username):
    mydb.open()
    pid = mydb.insert_db('INSERT INTO pattern (creator) VALUES (?)', [username])
    nid = mydb.insert_db('INSERT INTO node (pid, node_index) VALUES (?,?)', [pid, 1])
    mydb.query_db('UPDATE pattern SET connector = ? WHERE pid = ?', [nid, pid])
    mydb.close_db()
    return pid

def return_net():
    mydb.open()
    patterns = []
    results = mydb.query_db('SELECT * FROM pattern')


    for p in results:
        nodes = []
        nodes_results = mydb.query_db('SELECT * FROM node WHERE pid = ?', [p['pid']])
        # print "the nodes has %s node" % len(nodes_results)
        for n in nodes_results:
            tmp_node = Node(n['nid'], n['pid'], n['node_index'])
            nodes.append(tmp_node)

        nodes.sort()
        tmp_pattern = Pattern(p['pid'], p['connector'])
        tmp_pattern.nodes = nodes
        patterns.append(tmp_pattern)

    mydb.close_db()
    return patterns





