import MySQLdb
class revertScreen():
    def __init__(self):
        db = MySQLdb.connect(host='/tmp/mysql.sock/localhost',
                             user='root',
                             passwd='root',
                             db='spotify'
                            )
        cur = db.cursor()
        cur.execute("Select * from users")

        for row in cur.fetchall():
            print(row[0])
        db.close()