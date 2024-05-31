import datetime
import json
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

class dbInteraction():
    def __init__(self):
        if not firebase_admin._apps:
            cred = credentials.Certificate('/Users/danielwarren/Desktop/spotifyproject-89bac-firebase-adminsdk-yptt8-d9880283fd.json')
            app = firebase_admin.initialize_app(cred)
        global db
        db = firestore.client()

    def addUserToDB(self, userId):
        users = db.collection('users').get()
        ids = []
        for i in users:
            ids.append(i.id)
        if userId in ids:
            return
        else:
            doc = db.collection('users').document(userId)
            doc.set({
                'playlists': []
            })
    
    def addUserPlaylist(self, userId, playlist, dataFromPlaylist):
        playlistName = playlist['Playlist Name']
        trackCount = playlist['Track Count']

        userDBPlaylistIds = self.getUserDBPlaylistIds(userId)
        playlistId = userId + playlistName
        playlistId = "".join(playlistId.split()).replace(" ", "")
        
        #Check if playlist exists, if so add to firestore
        if playlistId not in userDBPlaylistIds:
            ref = db.collection('users').document(userId)
            hold = db.collection('playlists').document(playlistId)
            ref.update({'playlists': firestore.ArrayUnion([hold])})
            ref = db.collection('playlists').document(playlistId)
            ref.set({
                'playlistId': playlistId,
                'playlistName': playlistName,
                'versionCount': 1
            })
            versionId = playlistId + '1'
            ref = db.collection('playlists').document(playlistId).collection('versions').document(versionId)
            ref.set({
                'trackCount': trackCount,
                'Date Added': str(datetime.date.today()),
                'tracks': self.addTracks(playlistId=playlistId, holdData=dataFromPlaylist)
            })
            
        else:
            x = self.findMatchingVersion(playlistId, dataFromPlaylist)
            if not x['matchApi']:
                ref = db.collection('playlists').document(playlistId).collection('versions').document(x['versionId'])
                ref.set({
                    'trackCount': trackCount,
                    'Date Added': str(datetime.date.today()),
                    'tracks': self.addTracks(playlistId=playlistId, holdData=dataFromPlaylist)
                })
                return x['versionId']
            

    def addTracks(self, playlistId, holdData):
        x = json.loads(holdData)
        data = x['data']
        trackRefs = []
        for i in data:
            if 'LikedPlaylist' in playlistId:
                items = i['items']
            else:
                items = i['tracks']['items']

            for j in items:
                trackName = j['track']['name']
                trackId = j['track']['id']
                arts = j['track']['artists']
                holdArtNames = []
                holdArtIds = []
                for k in arts:
                    hold = k['name']
                    holdId = k['id']
                    holdArtNames.append(hold)
                    holdArtIds.append(holdId)
                ref = db.collection('tracks').document(trackId)
                ref.set({
                    'Track Name': trackName,
                    'Artist Names': holdArtNames,
                    'Artist Ids': holdArtIds
                })
                trackRefs.append(ref)
        return trackRefs
       
    def findMatchingVersion(self, playlistId, holdData):
        num = 1
        versionId = playlistId + str(num)
        x = json.loads(holdData)
        data = x['data']
        apiTrackIds = []
        f = open('holdData.json', 'w')
        for i in data:
            if 'LikedPlaylist' in playlistId:
                items = i['items']
            else:
                items = i['tracks']['items']

            for j in items:
                holdId = j['track']['id']
                apiTrackIds.append(holdId)
        ref = db.collection('playlists').document(playlistId).collection('versions').document(versionId).get()
        while ref.exists:
            match = True
            dbTracks = ref.to_dict()
            dbTracks = dbTracks['tracks']
            if len(dbTracks) != len(apiTrackIds):
                match = False
                num = num + 1
                versionId = playlistId + str(num)
                ref = db.collection('playlists').document(playlistId).collection('versions').document(versionId).get()
                continue
            else:
                for i in range(0, len(dbTracks)):
                    dbId = dbTracks[i].id
                    if dbId not in apiTrackIds[i]:
                        match = False
                        break
            if match:
                return {
                    'matchApi': True,
                    'versionId': versionId,
                    'tracks': self.addTracks(playlistId, holdData)
                }
            else:
                num = num + 1
                versionId = playlistId + str(num)
                ref = db.collection('playlists').document(playlistId).collection('versions').document(versionId).get()
        return {
            'matchApi': False,
            'versionId': versionId,
            'tracks': self.addTracks(playlistId, holdData)
        }  
    def getPlaylistVersionData(self, userId, playlistName):
        x = self.getUserDBPlaylistIds(userId)
        holdName = userId + playlistName.replace(' ', '')
        ref = None
        
        for i in x:
            if holdName in i:
                ref = db.collection('playlists').document(i)
        if ref == None:
            return None
        
        ref1 = ref.collection('versions').get()
        holdIds = []
        for i in ref1:
            holdIds.append(i.id)
        
        info = []
        for i in holdIds:
            ref1 = ref.collection('versions').document(i)
            versionId = ref1.id
            ref1 = ref1.get().to_dict()
            holdInfo = {
                'versionId': versionId,
                'dateAdded': ref1['Date Added'],
                'trackCount': ref1['trackCount'],
                'trackRefs': ref1['tracks']
            }
            info.append(holdInfo)
        return info
    
    def getUserDBPlaylistIds(self, userId):
        userPlaylists = db.collection('users').document(userId)
        doc = userPlaylists.get().to_dict()
        hold = []
        for i in doc['playlists']:
            hold.append(i.id)
        return hold

    def getTrackInfo(self, trackId):
        ref = db.collection('tracks').document(trackId).get().to_dict()
        artists = ''
        for i in ref['Artist Names']:
            artists = artists + ' ' + i
        return {
            'trackName': ref['Track Name'],
            'artists': artists
        }

    def savePlaylistVersion(self, trackInfo, playlistInfo):
        ref = db.collection('users').get()
        for i in ref:
            if i.id in playlistInfo['versionId']:
                userId = i.id
                break
            else:
                userId = 'Not Found'
        if userId == 'Not Found':
            return
        ref = db.collection('users').document(userId).get().to_dict()
        userPlaylists = ref['playlists']
        for i in range(0, len(userPlaylists)):
            if userPlaylists[i].id in playlistInfo['versionId']:
                playlistId = userPlaylists[i].id
                break
            else:
                playlistId = 'Not Found'

        if playlistId == 'Not Found':
            ref = db.collection('playlists').document(playlistInfo['versionId'])
            ref.update({
                'playlistId': playlistInfo['versionId'],
                'playlistName': playlistInfo['versionId'],
                'versionCount': 1
            })
        else:
            ref = db.collection('playlists').document(playlistId).collection('versions').get()
            length = len(ref)
            versionId = playlistId + str(length + 1)

            trackRefs = []
            
            for i in trackInfo:
                id = i['trackId']
                name = i['trackName']
                artistIds = i['Artist Ids']
                artistNames = i['Artist Names']
                ref = db.collection('tracks').document(id)
                trackRefs.append(ref)
                if not ref.get().exists:
                    ref.set({
                        'Track Name': name,
                        'Artist Ids': artistIds,
                        'Artist Names': artistNames
                    })
            ref = db.collection('playlists').document(playlistId).collection('versions').document(versionId)
            ref.set({
                'Date Added': str(datetime.date.today()),
                'trackCount': len(trackRefs),
                'tracks': trackRefs
            })

