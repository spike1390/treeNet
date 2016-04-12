import sqlite3

con = sqlite3.connect('test.db')
f = open('reset.sql','r')
str = f.read()
con.executescript(str)
con.close()
