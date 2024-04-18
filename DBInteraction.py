import requests
import MySQLdb

class dbInteraction():
    def inputValueToUsers(self, tableName, column, value):
        db = MySQLdb.connect(host='localhost',
                             user = 'root',
                             passwd='root',
                             db='spotify'
                            )
        cur = db.cursor()
        query = f'Select userId from users where userId = \"{value}\";'
        print(query)
        cur.execute(query)

        if not cur.fetchone():
            query = f'Insert into {tableName}({column}) values(\"{value}\");'
            cur.execute(query)
            db.commit()
    def getPlaylistTable(self, userId):
        db = MySQLdb.connect(host='locatlhost',
                             user='root',
                             passwd='root',
                             db='spotify'
                            )
        cur = db.cursor()
        

        query = f'select * from playlists where owner={userId};'
        x = cur.execute(query)
        cur.close()
        db.close()
        return x
    
    def getPlaylistInfo(self, userId, playlist):
        db = MySQLdb.connect(host='locatlhost',
                             user='root',
                             passwd='root',
                             db='spotify'
                            )
        cur = db.cursor()

        query = f'select * from tracks where owner={userId} and playlistName={playlist}'
        return cur.execute(query)