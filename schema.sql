
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


CREATE TABLE IF NOT EXISTS node(
	nid INTEGER PRIMARY KEY autoincrement,
	node_index INTEGER NOT NULL,
	pid INTEGER NOT NULL
);



CREATE TABLE IF NOT EXISTS message(
mid        INTEGER PRIMARY KEY      NOT NULL,
from_id    INTEGER                  NOT NULL,
to_id      INTEGER                  NOT NULL,
msg        TEXT,
status     INTEGER                  NOT NULL
);
