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
                self.cur.execute("INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", d)
                inserted += 1
            except sqlite3.IntegrityError:
                print "Failed insert:"
                print d
                skipped += 1
                continue
            except Exception as e:
                print "Generic fail:"
                print d
                print "Exception: "
                print e
                skipped += 1
                continue
        self.conn.commit()
        return (inserted, skipped)

    def getProblematicCustomers(self):
        '''Find the customers who have something not right'''
        self.cur.execute("SELECT name, lastname, address, certificatedate, 0 FROM customers WHERE (certificatedate < date('now') OR certificatedate IS NULL) AND membershiptype != 'cus' AND membershipyear >= strftime('%Y', 'now');")
        res = self.cur.fetchall()
        return dict(zip( range(1, len(res)+1), res))

    def findCustomer(self, hint):
        '''Find customers based on the hint'''
        self.cur.execute("SELECT name, lastname, address, certificatedate, 0 FROM customers WHERE name LIKE ? || '%' OR lastname LIKE ? || '%' OR address LIKE '%' || ? || '%' OR membernum LIKE ? || '%'", [hint for x in range(4)])
        res = self.cur.fetchall()
        return dict(zip( range(1, len(res)+1), res))

    def __del__(self):
        print "Closing conn"
        self.cur.close()
        del self.cur
        self.conn.close()
        del self.conn
