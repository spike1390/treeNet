# -*- coding: utf-8 -*-
import mydb,random,PathFinder,time,json
from Message import message
from Node import Node
from operator import methodcaller
import global_v,netModel


def active_all_Nodes():
    mydb.open()
    result = mydb.insert_db('update node SET active=1')
    mydb.close_db()

# get all message from database, as objects
def view_all_message():
    message_list=[]
    mydb.open()
    result = mydb.query_db('select * from message', one=False)
    if result:
        for msg in result:
            m = message(msg['_from'], msg['_to'], msg['msg'], None, msg['createdAt'])
            message_list.append(m)

    mydb.close_db()
    return json.dumps(message_list, default=methodcaller("json"))



# get all message from database, as objects
def view_failed_message():
    return json.dumps(global_v.failed_msg, default=methodcaller("json"))






#send a message from node whose nid is_from to nid _to, status 1 means delivered, 0 means block
def store_message_in_database(_from, _to, msg):
    mydb.open()
    ISOTIMEFORMAT='%Y-%m-%d %X'
    createdTime=str(time.strftime( ISOTIMEFORMAT, time.localtime() ))
    result = mydb.insert_db('insert into message(_from,_to,msg,createdAt) values(?,?,?,?)',
                            [_from,_to,msg,createdTime])
    mydb.close_db()

# get all inactive node nid
def find_all_inactiveNode():
    mydb.open()
    # active =1 means it is active
    result = mydb.query_db('select * from node WHERE active=0', one=False)
    mydb.close_db()
    nidList=[]
    if result:
        for nid in result:
            nidList.append(nid['nid'])
    return nidList


def find_all_inactive_pid():
    mydb.open()
    # active =1 means it is active
    result = mydb.query_db('select pid from node WHERE active=0 AND node_index=1', one=False)
    mydb.close_db()
    pidList=[]
    if result:
        for node in result:
            pidList.append(node['pid'])
    return pidList

#check whther a path is valid, if a invalid node exist in the path, return false
def check_path_valid(invalid_node_list, path):
    s= (set(invalid_node_list) & set(path))
    return len(s)==0

def transform_list_toStr(path_list):
    string=''
    for i in path_list:
        string+=(str(i)+' ').encode('utf-8')
    return string[0:len(string)-1]

# Create node object from database by nid,
def get_node_byID(nid):
    mydb.open()
    # active =1 means it is active
    result = mydb.query_db('select pid,node_index from node WHERE nid=?',[nid], one=True)
    if result:
        # we only need pid, and node index for a node to find a path
        node=Node(nid,result['pid'],result['node_index'])
        return node
    mydb.close_db()
    return None


#  get all failed msg in this list
def get_resend_msg_list(nid):
    msg_list=[]
    for msg in global_v.failed_msg:
        if msg.blockedAt==int(nid):
            msg_list.append(msg)
    return json.dumps(msg_list, default=methodcaller("json"))

def add_node():
     mydb.open()
     nid = mydb.insert_db('INSERT INTO pattern (pid,node_index,active,x,y) VALUES (1,1,1,1,1)')
     mydb.close_db()

def verify_node(nid):
    mydb.open()
    result=mydb.query_db('select nid from node ')
    mydb.close_db()
    if result==None: return False
    else: return True

# Find msg object by msg id
def get_msg_byId(msgId):
    for m in global_v.msg_buffer:
        if msgId==m.msgId:
            return m
    return None

#  the current nid msg passing to
def check_node_in_path(pre_nid, cur_nid, msgId):
    inactive_node_list=find_all_inactiveNode()
    print pre_nid
    print cur_nid
    #  if the current node is deleted
    if not verify_node(cur_nid):
        return False

    # if the path is blocked
    if cur_nid in inactive_node_list:
        # if the msg can't be sent, move the msg in buffer into failed msg list. from id is the last valid
        # node nid in the path
        msg_in_buffer=get_msg_byId(msgId);
        # If can't find the msg in the buffer
        if msg_in_buffer==None:
            return False
        for msg_obj in global_v.msg_buffer:
            if msgId==msg_obj.msgId:
                failedMsg=message(pre_nid,msg_obj._to, msg_obj.msg,msg_obj.path,None,msg_obj.sender,msg_obj.msgId, cur_nid)
                global_v.failed_msg.append(failedMsg)
                global_v.msg_buffer.remove(msg_obj)

        print 'Block at node '+ str(cur_nid)
        return False
    else:
        # if current node is active
        msg_in_buffer=get_msg_byId(msgId);
        print msg_in_buffer
        if msg_in_buffer==None:
            # print "Can't find the node, msgId:"+ str(msgId)
            return False
        path=msg_in_buffer.path
        #  if this node is destination node and is active
        if(int(path[len(path)-1])==cur_nid):
            store_message_in_database(int(msg_in_buffer.sender), int(msg_in_buffer._to), str(msg_in_buffer.msg))
            global_v.msg_buffer.remove(msg_in_buffer)
            # print 'Message from '+ str(msg_in_buffer.sender) +' to ' + str(msg_in_buffer._to) +' is delivered '
            return True
        else:
            # print '->' +str(cur_nid)
            return True


if __name__ == "__main__":
    # print view_all_message()
    netModel.change_node_status(85,0)
    # print  global_v.failed_msg
    pass
    #active_all_Nodes()
    # change_node_status(4,0)
    # the path either the valid one or the shortest invalid one
    # path=PathFinder.send_msg(1,2,'dsadsadadasdasdsadasdasdasdsadasdadsadadasdasdsfda')



    # for nid in path:
    #     pre_index = path.index(nid)-1
    #     if pre_index<0:
    #         pre_index=0
    #     result=check_node_in_path(path[pre_index],nid)
    #     print 'curent:'+ str(nid)
    #     print result
    #     if not check_node_in_path(path[pre_index],nid):
    #         break
    #change_node_status(2,0)
    #
    #
    # for msg in view_all_message():
    #     print 'from %s to %s, msg:%s created at: %s ' %(msg._from,msg._to,msg.msg,msg.createdAt)


