import requests
from io import StringIO
from DBInteraction import *
from tkinter import *

class cleanByArt():
    def __init__(self, frame, playlist, auth):
        global authItems
        global db
        db = dbInteraction()
        authItems = auth
        if playlist['Playlist Name'] == 'Liked Playlist':
            x = self.getDataFromLiked()
        else:
            print('Do something')
        length = len(x)
        lb = Listbox(frame, selectmode=MULTIPLE, height=length, width=200)
        confirm = Button(frame, text='Confirm', command=lambda: self.confirm(frame, lb, x, playlist))
        for i in x:
            name = i['artistName']
            trackCount = len(i['artistTracks'])
            add = f'{name} {trackCount}'
            lb.insert(END, add)
        confirm.pack()
        lb.pack()

    def confirm(self, frame, lb, data, playlist):
        selected = lb.curselection()
        selected = [lb.get(i) for i in selected]
        #Load current version of playlist into firebase
        #Delete Tracks from Playlist
        userId = self.getUserId()
        db.addUserPlaylist(userId, playlist)
        artists = []

        for i in selected:
            name = i[0:int(i.rfind(' '))]
            artists.append(name)
        print(artists)

    def getDataFromLiked(self):
        url = 'https://api.spotify.com/v1/me/tracks?limit=50'
        header = {
            'Authorization': authItems['type'] + ' ' + authItems['accessTok']
        }

        r = requests.get(url=url, headers=header)
        x = json.loads(r.text)
        next = x['next']

        f = open('holdData.json', 'w')
        f.write('{\n\"data\": [\n')
        while next != None:
            f.write('\t' + r.text + ',\n')
            url = next
            r = requests.get(url=url, headers=header)
            x = json.loads(r.text)
            next = x['next']
        f.write('\t' + r.text)
        f.write(']\n}')
        f.close()

        with open('holdData.json') as f:
            x = json.load(f)
            f.close()
        data = x['data']
        info = []
        trackArtists = []
        varArtCount = 1
        for i in data:
            items = i['items']
            for j in items:
                arts = j['track']['artists']
                for k in arts:
                    artistName = k['name']
                    if artistName not in trackArtists:
                        if artistName == '':
                            artistName = f'Various Artists {varArtCount}'
                            varArtCount = varArtCount + 1
                        artistId = k['id']
                        hold = self.getArtTracksFromLiked(data, artistName)
                        artistInfo = {
                            'artistName': artistName,
                            'artistId': artistId,
                            'artistTracks': hold['artistTracks'],
                            'artistTrackIds': hold['artistTrackIds']
                        }
                        info.append(artistInfo)
                        trackArtists.append(artistName)
        return info

    def getArtTracksFromLiked(self, data, artistName):
        tracks = []
        trackIds = []
        for i in data:
            items = i['items']
            for j in items:
                trackName = j['track']['name']
                trackId = j['track']['id']
                arts = j['track']['artists']
                for k in arts:
                    if k['name'] == artistName:
                        tracks.append(trackName)
                        trackIds.append(trackId)
                        break
        return {
            'artistTracks': tracks,
            'artistTrackIds': trackIds
        }

    def getUserId(self):
        url = 'https://api.spotify.com/v1/me'
        header = {
            'Authorization': authItems['type'] + ' ' + authItems['accessTok']
        }
        r = requests.get(url=url, headers=header)
        x = json.loads(r.text)
        return x['id']