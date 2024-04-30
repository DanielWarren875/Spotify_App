import json
import requests
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
#from firebase_admin import db

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
        print(docs)
        
        if userId in docs:
            return
        else:
            doc = db.collection('users').document(userId)
            doc.set({
                'playlists': []
            })
    
    def addUserPlaylist(self, userId, playlist):
        hold = f' {userId}'
        hold = playlist[0].split(hold)
        playlistName = hold[0]
        trackCount = hold[1]
        trackCount = trackCount[1:]

        userDBPlaylistIds = self.getUserDBPlaylistIds(userId)
        playlistId = userId + playlistName
        playlistId = "".join(playlistId.split())
        
        if playlistId not in userDBPlaylistIds:
            ref = db.collection('users').document(userId)
            ref.update({'playlists': firestore.ArrayUnion([playlistId])})
            ref = db.collection('playlists').document(playlistId)
            ref.set({
                'playlistId': playlistId,
                'playlistName': playlistName,
                'versionCount': 1
            })
            versionId = playlistName + '1'
            ref = db.collection('playlists').document(playlistId).collection('versions').document(versionId)
            trackCount = 0
            ref.set({
                'tracks': self.addTracks()
            })

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
        



            
            


    def getUserDBPlaylistIds(self, userId):
        userPlaylists = db.collection('users').document(userId)
        doc = userPlaylists.get().to_dict()

        return doc['playlists']

x = dbInteraction()
x.addTracks()