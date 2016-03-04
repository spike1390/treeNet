# -*- coding: utf-8 -*-
import sqlite3
import path



def open():

    global db
    db = sqlite3.connect(path.db_path)
    if db is None:
        print 'db not found'

def query_db(query, args=(), one=False):
    try:
        db

    except:
        open()

    cur = db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

def insert_db(query, args=()):
    try:
        db
    except:
        open()

    c = db.cursor()
    c.execute(query, args)
    db.commit()
    return c.lastrowid if c.lastrowid else None

def delete_db(query, args=()):
    try:
        db
    except:
        open()

    c = db.cursor()
    c.execute(query,args)
    db.commit()
    return c.lastrowid if c.lastrowid else None

def close_db():
    db.close()