import requests
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
#from firebase_admin import db

class dbInteraction():
    def __init__(self):
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
    
    def addUserPlaylists(self, userId, playlists):
        dbPlaylists = self.getUserPlaylists(userId)
    

    def getUserPlaylists(self, userId):
        ref = db.collection('users').document(userId)
        hold = ref.get().to_dict()
        dbPlaylists = hold['playlists']
        

x = dbInteraction()
x.getUserPlaylists('userId')