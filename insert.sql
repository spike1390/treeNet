INSERT INTO pattern (creator)
VALUES ('spikewang');
INSERT INTO pattern (creator)
VALUES ('spikewang');
INSERT INTO node (node_index, pid, id)
VALUES (1,1,'A0');
INSERT INTO node (node_index, pid,id)
VALUES (1,2,'B0');
INSERT INTO node (node_index, pid,id)
VALUES (2,1,'A1');
INSERT INTO node (node_index, pid,id)
VALUES (1,3,'C0');


INSERT INTO account (username, pwd, type, status)
VALUES ('vincent1','2cs744',0,1);

INSERT INTO edge (_from, _to)
VALUES (1,2);
INSERT INTO edge (_from, _to)
VALUES (2,3);


UPDATE account SET sq_1='',as_1='',sq_2='',as_2='',sq_3='',as_3=''
WHERE username = 'spike1390';
