import tkinter
import requests
from DBInteraction import *

class cleanByUser():
    def __init__(self, frame, playlist, auth):
        global authItems
        global db

        db = dbInteraction()
        authItems = auth
        self.clearFrame(frame)
        if playlist['Playlist Name'] == 'Liked Playlist':
            data = self.getData(playlist['Playlist Name'])
        else:
            data = self.getData(playlist['Playlist Name'])
        
    def getData(self, playlist):
        if playlist == 'Liked Playlist':
            url = 'https://api.spotify.com/v1/me/tracks?limit=50'
        else:
            print('This function is currently unavailable')
            return
        header = {
            'Authorization': authItems['type'] + ' ' + authItems['accessTok']
        }
        '''
        data = {
            'trackName': '',
            'trackId': '',
            'artists': [''],
            'albumName': '',
            'dateAdded': ''
        }
        '''
        data = []
        while url != None:
            r = requests.get(url=url, headers=header)
            x = json.loads(r.text)
            next = x['next']
            items = x['items']
            for i in items:
                dateAdded = i['added_at']
                trackName = i['track']['name']
                trackId = i['track']['id']
                albumName = i['track']['album']['name']
                arts = i['track']['artists']
                holdArtNames = []
                for j in arts:
                    holdName = j['name']
                    holdArtNames.append(holdName)
                info = {
                    'trackName': trackName,
                    'trackId': trackId,
                    'artists': holdArtNames,
                    'albumName': albumName,
                    'dateAdded': dateAdded
                }
                data.append(info)
            url = next
        return data

    def clearFrame(self, frame):
        for i in frame.winfo_children():
            i.destroy()