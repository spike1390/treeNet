import mydb, sqlite3
from models import accessControl
print mydb.DATABASE

mydb.insert_db("""update account SET pwd = ? WHERE username = ? """,
          ('wzs','spikewang'))

print accessControl.verify('spikewang','dsd').name