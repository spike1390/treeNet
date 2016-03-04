
CREATE TABLE IF NOT EXISTS account(
	username TEXT PRIMARY KEY NOT NULL,
	pwd TEXT NOT NULL,
	type INTEGER NOT NULL,
	sq_1 TEXT,
	as_1 TEXT,
	sq_2 TEXT,
	as_2 TEXT,
	sq_3 TEXT,
	as_3 TEXT,
	status INTEGER
);



CREATE TABLE IF NOT EXISTS pattern(
	pid INTEGER PRIMARY KEY autoincrement,
	connector INTEGER,
	creator TEXT NOT NULL,
  	FOREIGN KEY(creator) REFERENCES account(username)
);


CREATE TABLE node(
nid INTEGER PRIMARY KEY autoincrement,
node_index INTEGER NOT NULL,
pid INTEGER NOT NULL
, x INTEGER, y INTEGER, active INTEGER, id varchar(20)
);


CREATE TABLE edge IF NOT EXISTS edge(
	_from INTEGER NOT NULL,
	_to INTEGER NOT NULL,
	FOREIGN KEY(_from) REFERENCES pattern(pid),
	FOREIGN KEY(_to) REFERENCES pattern(pid),
	PRIMARY KEY (_from, _to)
);

CREATE TABLE IF NOT EXISTS message(
	mid INTEGER PRIMARY KEY autoincrement,
	_from INTEGER NOT NULL,
	_to INTEGER NOT NULL,
	msg TEXT,
	status INTEGER NOT NULL,
	FOREIGN KEY(_from) REFERENCES node(nid),
	FOREIGN KEY(_to) REFERENCES node(nid)
);





