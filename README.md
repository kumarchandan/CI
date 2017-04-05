
I got some help here

http://stackoverflow.com/questions/25387537/sqlite3-operationalerror-near-syntax-error
cur = self.con.execute("select rowid from {} where {}=?".format(table, field), (value,))    # sql parameters can't be set using ?, use .format()

http://pythoncentral.io/introduction-to-sqlite-in-python/


# Sqlite stuffs
to show databae : $.databases

to show tables : $.tables

to attach to a database: $attach database 'dbname.sqlite' as 'db'

