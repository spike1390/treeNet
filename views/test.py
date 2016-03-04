from models import accessControl
from models import netModel
from models import mydb
import json
from models import Node




u = 'ew'.encode('utf8')
p = 'dsa'.encode('utf8')
re = accessControl.verify(u, p)
print re


# u = User('s','d','ds')
#
# p = Pattern(2,u)
#
# print p.connect.name

mydb.insert_db('update ')
print accessControl._valid_login_format('spike1390', '2cs744')
# l = [Node(21,4,3), Node(1,2,5), Node(2,4,2)]
# l.sort()
# for u in l:
#     print u.index
# re = accessControl.verify('spikewang', 'cs744')
# print re.name



r2 = accessControl.verify('spikewang', 'cs7dsd44')
# print r2.name

ps = netModel.return_net()

lis = [2,3,4]
for i in range(0,len(lis)):
    print lis[i]

print json.dumps(ps, default = methodcaller("json"))

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

print dis_string
print json.dumps(dis_string)
    # json_string = json.dumps([ob.__dict__ for ob in p.nodes])
    #
    # print json_string



