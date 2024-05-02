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
        users = db.collection('users')
        docs = users.stream()
        
        if userId in docs:
            return
        else:
            doc = db.collection('users').document(userId)
            doc.set({
                'playlists': []
            })
    
    def addUserPlaylist(self, userId, playlist):
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
                'tracks': self.addTracks()
            })
        else:
            x = self.findMatchingVersion(playlistId)
            print(x)
            if not x['matchApi']:
                ref = db.collection('playlists').document(playlistId).collection('versions').document(x['versionId'])
                ref.set({
                    'trackCount': trackCount,
                    'Date Added': str(datetime.date.today()),
                    'tracks': self.addTracks()
                })
                return x['versionId']
            

    def addTracks(self):
        f = open('holdData.json', 'r')
        x = json.load(f)

        data = x['data']
        trackRefs = []
        for i in data:
            items = i['items']
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
       
    def findMatchingVersion(self, playlistId):
        num = 1
        versionId = playlistId + str(num)
        
        f = open('holdData.json', 'r')
        x = json.load(f)
        data = x['data']
        apiTrackIds = []
        for i in data:
            items = i['items']
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
                    'tracks': self.addTracks()
                }
            else:
                num = num + 1
                versionId = playlistId + str(num)
                ref = db.collection('playlists').document(playlistId).collection('versions').document(versionId).get()
        return {
            'matchApi': False,
            'versionId': versionId,
            'tracks': self.addTracks()
        }  


    def getUserDBPlaylistIds(self, userId):
        userPlaylists = db.collection('users').document(userId)
        doc = userPlaylists.get().to_dict()
        hold = []
        for i in doc['playlists']:
            hold.append(i.id)
        return hold