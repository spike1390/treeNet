# -*- coding: utf-8 -*-
import mydb,random,PathFinder,time,json
from Message import message
from Node import Node
from operator import methodcaller
import global_v

# Randomly choose one active node to be inactive and return all active node return nid list
def randomly_inactive_node(seed):
    num=random.randint(0,100)
    if(num<seed):
        mydb.open()
    # active =1 means it is active
        result = mydb.query_db('select * from node WHERE active=1', one=False)
        mydb.close_db()
        nidList=[]
        if result:
            for nid in result:
                nidList.append(nid['nid'])
            inactive_nid=nidList[random.randint(0, len(nidList)-1)]
        # set not whose nid is inactive_nid to inactive status, pass nid and inactive(0)
            change_node_status(inactive_nid,0)
        # return a random nid as inactive node
            return find_all_inactiveNode()

def active_all_Nodes():
    mydb.open()
    result = mydb.insert_db('update node SET active=1')
    mydb.close_db()

# active a inactive node. input must be a inactive node's nid
def change_node_status(nid, active):
    mydb.open()
    # active =1 means it is active
    result = mydb.insert_db('update node SET active=?  WHERE nid=?',[active,nid])
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


#send a message from node whose nid is_from to nid _to, status 1 means delivered, 0 means block
def send_message(_from, _to, msg):
    mydb.open()
    ISOTIMEFORMAT='%Y-%m-%d %X'
    createdTime=str(time.strftime( ISOTIMEFORMAT, time.localtime() ))
    result = mydb.insert_db('insert into message(_from,_to,msg,createdAt) values(?,?,?,?)',
                            [_from,_to,msg,createdTime])
    mydb.close_db()


# get all failed message and
# def get_all_failed_message():
#     message_list=[]
#     mydb.open()
#     result = mydb.query_db('select * from message WHERE status=0', one=False)
#     for msg in result:
#         message_list.append(message(msg['mid'],msg['path'],msg['_from'],msg['_to']))
#     mydb.close_db()
#     return message_list


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


# Everytime when user active a node , check whther the massage can be sent.
# And put them in the global_v.can_be_deliver
def get_can_be_resent_msgList( ):
    #  get all inactive node as inactive_nid_list
    inactive_nid_list=find_all_inactiveNode()
    #  get list of failed msg objects
    failed_message=global_v.failed_msg
    for msg_obj in failed_message:
        node1=get_node_byID(msg_obj._from)
        node2=get_node_byID(msg_obj._to)
        # re find the path beetwwen two node , and check whether the path is valid
        path=PathFinder.find_message_path(node1,node2,msg_obj.msg)
        # if the path is valid, update the message
        resent_msg_list=[]
        if check_path_valid(inactive_nid_list, path):
            #  if the failed msg can be deliver this time, store it in can_be_deliver list
            global_v.failed_msg.remove(msg_obj)
            global_v.can_be_deliver.append(msg_obj)


# Create node object from database by nid,
def get_node_byID(nid):
    mydb.open()
    # active =1 means it is active
    result = mydb.query_db('select pid,node_index from node WHERE nid=?',[nid], one=True)
    mydb.close_db()
    if result:
        # we only need pid, and node index for a node to find a path
        node=Node(nid,result['pid'],result['node_index'])
        return node
    return None


#  active a inactive node, and resend all valid msg again
def active_node(nid):
    change_node_status(nid,1)
    print 'Node '+ str(nid) + ' has been actived'
    get_can_be_resent_msgList()
    #  start to check whther can send msg again
    for msg in global_v.can_be_deliver:
        node1=get_node_byID(msg._from)
        node2=get_node_byID(msg._to)
        print node1.nid
        path=PathFinder.find_message_path(node1,node2,' msg tesing !!!')
        print 'new path'
        print path
        for nid in path:
            pre_index=path.index(nid)-1
            if pre_index<0:
                pre_index=0
            if not check_node_in_path(path[pre_index],nid):
                break

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

#  the current nid msg passing to
def check_node_in_path(pre_nid, cur_nid):
    inactive_node_list=find_all_inactiveNode()
    #  if the current node is deleted
    if not verify_node(cur_nid):
        return False

    # if the path is blocked
    if cur_nid in inactive_node_list:
        # if the msg can't be sent, move the msg in buffer into failed msg list. from id is the last valid
        # node nid in the path
        newPath=[]
        msg_in_buffer=global_v.msg_buffer[0];
        newPath = PathFinder.refind_path(pre_nid,msg_in_buffer._to)
        #  if there is no any new path, then stop
        # either the destination or start node is deleted , new Path is none

        if newPath==None:
            print 'Block at node '+ str(cur_nid)
            return False

        # if the new path is valid,
        if check_path_valid(inactive_node_list, newPath):
            print 'new path'
            print newPath
            return False
        else:
             # the new path is
             print 'Block at node '+ str(cur_nid)
             return False

        failed_msg = message(pre_nid, msg_in_buffer._to, msg_in_buffer.msg)
        del global_v.msg_buffer[0]
        global_v.failed_msg.append(failed_msg)
        print 'Block at node '+ str(cur_nid)
        return False
    else:
        # if current node is active
        msg_in_buffer=global_v.msg_buffer[0];
        path=msg_in_buffer.path
        #  if this node is destination node and is active
        if(int(path[len(path)-1])==cur_nid):
            msg = message(pre_nid, msg_in_buffer._to, msg_in_buffer.msg)
            send_message(msg_in_buffer._from, msg_in_buffer._to, msg_in_buffer.msg)
            print 'Message from '+ str(msg_in_buffer._from) +' to ' + str(msg_in_buffer._to) +' is delivered '
            return True
        else:
            print '->' +str(cur_nid)
            return True




if __name__ == "__main__":
    # print view_all_message()
    pass
    # active_all_Nodes()
    # change_node_status(6,0)
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


