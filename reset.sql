drop table pattern;
drop table node;
drop table edge;
drop table domain;

CREATE TABLE IF NOT EXISTS domain(
	did INTEGER PRIMARY KEY autoincrement,
	creator TEXT NOT NULL

);

CREATE TABLE IF NOT EXISTS pattern(
	pid INTEGER PRIMARY KEY autoincrement,
	connector INTEGER,
	did INTEGER NOT NULL,
	isDomain INTEGER NOT NULL,
  	FOREIGN KEY(did) REFERENCES domain(did)

);


CREATE TABLE IF NOT EXISTS node(
nid INTEGER PRIMARY KEY autoincrement,
node_index INTEGER NOT NULL,
pid INTEGER NOT NULL,
active INTEGER
);

CREATE TABLE IF NOT EXISTS edge(
	_from INTEGER NOT NULL,
	_to INTEGER NOT NULL,
	FOREIGN KEY(_from) REFERENCES pattern(pid)
	FOREIGN KEY(_to) REFERENCES pattern(pid)
	PRIMARY KEY (_from, _to)
);
-- domain 1
INSERT INTO domain (creator)
VALUES ('spikewang');
INSERT INTO pattern (did,isDomain)
VALUES (1,1);
INSERT INTO node (node_index, pid, active)
VALUES (1,1,1);
INSERT INTO pattern (did,isDomain)
VALUES (1,0);
INSERT INTO pattern (did,isDomain)
VALUES (1,0);
INSERT INTO pattern (did,isDomain)
VALUES (1,0);
INSERT INTO node (node_index, pid, active)
VALUES (1,2,1);
INSERT INTO node (node_index, pid, active)
VALUES (1,3,1);
INSERT INTO node (node_index, pid, active)
VALUES (2,2,1);
INSERT INTO node (node_index, pid, active)
VALUES (1,4,1);
INSERT INTO edge (_from, _to)
VALUES (1,2);
INSERT INTO edge (_from, _to)
VALUES (1,3);
INSERT INTO edge (_from, _to)
VALUES (1,4);
INSERT INTO edge (_from, _to)
VALUES (2,3);
-- domain 2
INSERT INTO domain (creator)
VALUES ('spikewang');
INSERT INTO pattern (did,isDomain)
VALUES (2,1);
INSERT INTO node (node_index, pid, active)
VALUES (1,5,1);
INSERT INTO pattern (did,isDomain)
VALUES (2,0);
INSERT INTO node (node_index, pid, active)
VALUES (1,6,1);
INSERT INTO edge (_from, _to)
VALUES (5,6);
-- domain 1 connceted to domain 2
INSERT INTO edge (_from, _to)
VALUES (1,5);

UPDATE node SET active = 0 WHERE nid = 2;


drop table message;

CREATE TABLE IF NOT EXISTS message(
	mid INTEGER PRIMARY KEY autoincrement,
	_from INTEGER NOT NULL,
	_to INTEGER NOT NULL,
	msg TEXT,
	createdAt TEXT,
	FOREIGN KEY(_from) REFERENCES node(nid),
	FOREIGN KEY(_to) REFERENCES node(nid)
);

