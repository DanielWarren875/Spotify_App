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

    def addPlaylistTracks(self, userId, playlistId, tracks):
        count = 1
        versionId = userId + playlistId + str(count)
        versionId = "".join(versionId.split())

        while True:
            ref = db.collection('playlists').document(playlistId).collection('playlistVersions').document(versionId)
            doc = ref.get()
            if doc.exists:
                count = count + 1
                versionId = userId + playlistId + str(count)
                versionId = "".join(versionId.split())
            else:
                break
        
        ref = db.collection('playlists').document(playlistId).collection('playlistVersions').document(versionId)
        ref.set({
            'trackCount': len(tracks),
            'trackIds': []
        })
        
        



            
            


    def getUserDBPlaylistIds(self, userId):
        userPlaylists = db.collection('users').document(userId)
        doc = userPlaylists.get().to_dict()

        return doc['playlists']
