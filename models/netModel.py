import mydb, json
from Node import Node,edge,pattern

from operator import methodcaller
import json_test




def return_json():
    return json_test.return_json()

def add_domain(ds):
    mydb.open()
    did = mydb.insert_db('INSERT INTO domain (creator) VALUES (?)',['spikewang'])
    print did
    d_pid = mydb.insert_db('INSERT INTO pattern (did, isDomain) VALUES (?,1)', [did])
    d_nid = mydb.insert_db('INSERT INTO node (pid, node_index, active) VALUES (?,1,1)', [d_pid])
    pid = mydb.insert_db('INSERT INTO pattern (did, isDomain) VALUES (?,0)', [did])
    nid = mydb.insert_db('INSERT INTO node (pid, node_index, active) VALUES (?,1,1)', [pid])
    for d in ds:
        d_pattern = mydb.query_db('SELECT * FROM pattern WHERE did = ? and isDomain = 1', [d], one = True)
        mydb.insert_db('INSERT INTO  edge(_from, _to) VALUES (?,?)', [d_pid, d_pattern['pid']])
    mydb.insert_db('INSERT INTO  edge(_from, _to) VALUES (?,?)', [d_pid, pid])
    mydb.close_db()
    return (did, pid, nid, d_nid)

def add_pattern(ps, did):
    mydb.open()
    d_pattern = mydb.query_db('SELECT * FROM pattern WHERE did = ? and isDomain = 1', [did], one = True)
    pid = mydb.insert_db('INSERT INTO pattern (did, isDomain) VALUES (?,0)', [did])
    nid = mydb.insert_db('INSERT INTO node (pid,node_index,active) VALUES (?,1,1)', [pid])
    mydb.insert_db('INSERT INTO  edge(_from, _to) VALUES (?,?)', [pid, d_pattern['pid']])
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


def delete_domain(pid, did):
    mydb.open()
    d_pattern = mydb.query_db('SELECT * FROM pattern WHERE did = ? and isDomain = 1', [did], one = True)
    mydb.delete_db('delete from edge where _from = ? or _to = ?',[d_pattern['pid'], d_pattern['pid']])
    mydb.delete_db('delete from domain where did=?', [did])
    mydb.delete_db('delete from pattern where pid=?', [d_pattern['pid']])
    mydb.delete_db('delete from node where pid=?', [d_pattern['pid']])
    mydb.delete_db('delete from pattern where pid=?', [pid])
    mydb.delete_db('delete from node where pid=?', [pid])
    mydb.close_db()
    return True

def delete_pattern(pattern_id):
    mydb.open()
    mydb.delete_db('delete from edge where _from = ? or _to = ?',[pattern_id, pattern_id])
    mydb.delete_db('delete from pattern where pid=?', [pattern_id])
    mydb.delete_db('delete from node where pid=? and node_index = 1', [pattern_id])
    mydb.close_db()
    return True



def change_node_status(nid, active):
    mydb.open()
    # active =1 means it is active
    result = mydb.insert_db('update node SET active=?  WHERE nid=?', [active,nid])
    mydb.close_db()


def delete_connection(nid1,nid2):
    mydb.open()
    p1 = mydb.query_db('SELECT * FROM node WHERE nid = ?', [nid1], one = True)
    p2 = mydb.query_db('SELECT * FROM node WHERE nid = ?', [nid2], one = True)
    mydb.delete_db('delete from edge where _from = ? and _to = ?',[p1['pid'], p2['pid']])
    mydb.delete_db('delete from edge where _from = ? and _to = ?',[p2['pid'], p1['pid']])
    mydb.close_db()
    pass

def add_connection(nid1,nid2):
    mydb.open()
    p1 = mydb.query_db('SELECT * FROM node WHERE nid = ?', [nid1], one = True)
    p2 = mydb.query_db('SELECT * FROM node WHERE nid = ?', [nid2], one = True)
    mydb.insert_db('INSERT INTO  edge(_from, _to) VALUES (?,?)', [p1['pid'], p2['pid']])

    mydb.close_db()
    pass


# print add_domain([1,2])
#delete_pattern(4)
# print return_json()
#print add_node(4,3)
# delete_node([7,8,9])
# print add_pattern([1,2])[1]
# add_node(4,3)
# print delete_pattern(4)

