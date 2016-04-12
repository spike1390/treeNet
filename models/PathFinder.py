import mydb, global_v, SendMessage
from Node import Node
from Message import message



def getPathFromRoot(node):
        path = []
        index=node.index
        while (index!=0):
          path.append(index)
          index=index/2
        path.reverse()
        return path

# find path in one tree, using index in the tree.
def get_path_inTree(nd1, nd2):
    if nd1.pid==nd2.pid and nd1.index==nd2.index:
        path=[nd1.index,nd2.index]
        return path
    path_1 = getPathFromRoot(nd1)
    path_2 = getPathFromRoot(nd2)

    for i in range(0, max(len(path_1), len(path_2))):
        if i == min(len(path_1) , len(path_2)) or path_1[i] != path_2[i] :
            total_path = path_1[i:]
            total_path.reverse()
            total_path.extend(path_2[i-1:])
            return total_path

def transform_to_nidList(pid, path):
    nidList=[]
    mydb.open()
    for index in path:
        query='select nid from node WHERE pid=? AND node_index= ?'
        result = mydb.query_db(query,[str(pid),index], one = True)
        if not result==None:
            nidList.append(result['nid'])
    mydb.close_db()
    return nidList



# graph = {'A': ['B','D','E'],
#              'B': ['A','G'],
#              'C': ['E','F','G'],
#              'D': ['F','A'],
#              'E': ['A','C'],
#              'F': ['C','D']}


def get_shortest_path(graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        if not graph.has_key(start):
            return None
        shortest = None
        for node in graph[start]:
            if node not in path:
                newpath = get_shortest_path(graph, node, end, path)
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
        return shortest

def generate_graph():
    mydb.open()
    graph= dict()
    query = 'select * from edge'
    result = mydb.query_db(query, one = False)
    mydb.close_db()
    inactive_pid_list=SendMessage.find_all_inactive_pid()
    if not result==None:
        for r in result:
            f=r['_from']
            t=r['_to']
            if not f in inactive_pid_list and not t in inactive_pid_list:
                # if the key is not exist in the graph
                if f not in graph:
                   graph[f]=[t]
                else:
                   temp_List=graph[f]
                   temp_List.append(t)
                if t not in graph:
                    graph[t]=[f]
                else:
                    temp_List=graph[t]
                    temp_List.append(f)
                # print str(r['_from'])+' to '+ str(r['_to'])
    return graph

def generate_blocked_graph():
    mydb.open()
    graph= dict()
    query = 'select * from edge'
    result = mydb.query_db(query, one = False)
    mydb.close_db()
    inactive_pid_list=SendMessage.find_all_inactive_pid()
    if not result==None:
        for r in result:
            f=r['_from']
            t=r['_to']
            # if the key is not exist in the graph
            if f not in graph:
                graph[f]=[t]
            else:
                temp_List=graph[f]
                temp_List.append(t)
            if t not in graph:
                graph[t]=[f]
            else:
                temp_List=graph[t]
                temp_List.append(f)
                # print str(r['_from'])+' to '+ str(r['_to'])
    return graph

# path entry, start end is the pid
def find_path_nidList(start, end, bloked):
    pidList=[]
    if not bloked:
        pidList=get_shortest_path(generate_graph(),start,end)
    else:
        pidList=get_shortest_path(generate_blocked_graph(),start,end)
    # del pidList[0]
    # del pidList[len(pidList)-1]
    nidList=[]
    mydb.open()
    if pidList:
      for pid in pidList:
        query='select nid from node WHERE pid=? AND node_index=1'
        result = mydb.query_db(query,[str(pid)], one = True)
        if not result==None:
            nidList.append(result['nid'])
    mydb.close_db()
    return nidList

# find a path from one node to the root node
def get_path_to_root(node):
    s = []
    while node:
        s.append(node)
        node = node.parent
    return reversed(s)

def get_path(node1, node2):
    if node1 == node2:
        return 1
    s1 = get_path_to_root(node1)
    s2 = get_path_to_root(node2)
    if len(s1) == 1:
        return s1
    if len(s2) == 1:
        return s2
    for i in xrange(0, len(s1)):
        if i >= len(s1) or i >= len(s2) or s1[i] != s2[i]:
            return reversed(s1[i:]) + s2[i - 1:]


# find a path between two nodes
def find_message_path(node1,node2 ):
    # if the two nodes are in one pattern
    if node1.pid==node2.pid:
        return transform_to_nidList(node1.pid,get_path_inTree(node1,node2))

    # if two nodes are from different tree
    path=[]
    root=Node(0,0,1)
    path1=[]
    path2=[]
    path3=[]
    # if from node is not connector node
    if(node1.index!=1):
        path1=transform_to_nidList(node1.pid, get_path_inTree(node1,root))

    # fisrt find any shortest valid path.
    path2=find_path_nidList(node1.pid,node2.pid,False);
    #  if any path bewteen two connector is blocked, then choose a shortest blocked one
    if len(path2)==0:
        path2=find_path_nidList(node1.pid,node2.pid,True);
    #  if the destination is not the connector node, then find path inside the tree
    if(node2.index!=1):
        path3=transform_to_nidList(node2.pid, get_path_inTree(root,node2))
    path=path1+path2+path3
    # remove duplicate element in the path
    l2 = list(set(path))
    l2.sort(key=path.index)

    # msg=message(node1.nid,node2.nid,msg, l2)
    # global_v.msg_buffer.append(msg)
    return l2
    #path2=find_path_nidList

#  refind a path
def refind_path(nid1,nid2):
    node1=SendMessage.get_node_byID(nid1)
    if node1==None: return None
    node2=SendMessage.get_node_byID(nid2)
    if node2==None: return None
    path=find_message_path(node1,node2)
    return path



def send_msg(nid1, nid2, msg, msgId):
    node1=SendMessage.get_node_byID(nid1)
    if node1==None: return 'from node does not exist'
    node2=SendMessage.get_node_byID(nid2)
    if node2==None: return 'destination node does not exist'

    #  If it is failed msg to be resend , delete it from failed msg list first
    senderId=node1.nid
    path=find_message_path(node1,node2)
    for msg_obj in global_v.failed_msg:
        if msgId==msg_obj.msgId:
            senderId=msg_obj.sender
            global_v.failed_msg.remove(msg_obj)
            break
    msg_pending=message(node1.nid,node2.nid, msg, path,None,senderId, int(msgId))
    global_v.msg_buffer.append(msg_pending)
    return path


# print generate_graph()
# print find_path_nidList(1,6)
# print test_findNid_pid('1')

if __name__ == "__main__":
    pass
    # root1=Node(0,2,1)
    # root2=Node(0,6,5)
    # path = get_path_inTree(root1, root2)
    # print find_message_path(root1,root2)
