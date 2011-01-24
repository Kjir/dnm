import sqlite3

class Connection:
    def __init__(self, dbname):
        self.conn = sqlite3.connect(dbname)
        self.cur = self.conn.cursor()

    def createTables(self):
        f = open("sql/create_customers.sql", 'r')
        self.cur.execute(f.read())

    def __del__(self):
        print "Closing conn"
        self.cur.close()
        del self.cur
        self.conn.close()
        del self.conn
