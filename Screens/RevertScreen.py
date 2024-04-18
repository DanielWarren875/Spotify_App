import json
import MySQLdb
import requests
class revertScreen(): 
    def loadData(self, authItems):
        add = []
        url = 'https://api.spotify.com/v1/me/tracks'
        auth = authItems.getAuthItems()
        header = {
            'Authorization': auth['type'] + ' ' + auth['accessTok']
        }
        r = requests.get(url=url, headers=header)
        x = json.loads(r.text)
        items = x['items']
        playlistName = 'Liked Playlist'
        versionNum = 1

        for i in items:
            trackName = i['track']['name']
            trackId = i['track']['id']
            arts = i['track']['artists']
            artists = ''
            for j in arts:
                artists = artists + ' ' + j['name']
            hold = {
                'playlistName': playlistName,
                'versionNum': versionNum,
                'trackName': trackName,
                'trackId': trackId,
                'artists': artists
            }
            add.append(hold)
        db = MySQLdb.connect(host='localhost',
                             user='root',
                             passwd='root',
                             db='spotify'
                            )
        cur = db.cursor()
        playlistName = hold['playlistName']
        versionNum = hold['versionNum']
        trackName = hold['trackName']
        trackId = hold['trackId']
        artists = hold['artists']
        userId = auth['UserId']

        query = f'Insert into users(userId) values(\"{userId}\");'
        cur.execute(query)
        db.commit()

        query = f'Insert into playlists(owner, playlistName, versionNum) values(\"{userId}\",\"Liked Playlist\", 1);'
        cur.execute(query)
        db.commit()

        query = f'Insert into tracks(playlistName, versionNum, trackName, artists, trackId) values (\"{playlistName}\", {versionNum}, \"{trackName}\", \"{trackId}\",\"{artists}\");'
        cur.execute(query)
        db.commit()