import mydb, sqlite3
from models import accessControl


# mydb.insert_db("""update account SET pwd = ? WHERE username = ? """,
#           ('wzs','spikewang'))
#
# print accessControl.verify('spikewang','dsd').name
mydb.open()
id = 'A0'
mydb.insert_db("""UPDATE node SET x=? WHERE id = ? """, (2, id))
mydb.close_db()