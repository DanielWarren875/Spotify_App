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
                'tracks': self.addTracks()
            })
        else:
            self.findMatchingVersion(playlistId)

    def addTracks(self):
        f = open('holdData.json', 'r')
        x = json.load(f)

        data = x['data']
        trackRefs = []
        count = 0
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
        
        ref = db.collection('playlists').document(playlistId).collection('versions').document(versionId).get()
        
        while ref.exists:
            print(versionId + ' exists\n')
            num = num + 1
            versionId = playlistId + str(num)
            ref = db.collection('playlists').document(playlistId).collection('versions').document(versionId).get()

        print(versionId + ' does not exist')
            
            


    def getUserDBPlaylistIds(self, userId):
        userPlaylists = db.collection('users').document(userId)
        doc = userPlaylists.get().to_dict()

        return doc['playlists']