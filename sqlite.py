import sqlite3

class Connection:
    def __init__(self, dbname):
        self.conn = sqlite3.connect(dbname)
        self.cur = self.conn.cursor()

    def createTables(self):
        f = open("sql/create_customers.sql", 'r')
        self.cur.execute(f.read())

    def insertCustomers(self, data):
        inserted = 0
        skipped = 0
        for d in data:
            try:
                self.cur.execute("INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", d)
                inserted += 1
            except sqlite3.IntegrityError:
                print "Failed insert:"
                print d
                skipped += 1
            except:
                print "Generic fail:"
                print d
                skipped += 1
        self.conn.commit()
        return (inserted, skipped)

    def __del__(self):
        print "Closing conn"
        self.cur.close()
        del self.cur
        self.conn.close()
        del self.conn
