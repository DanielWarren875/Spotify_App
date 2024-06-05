import requests
from io import StringIO
from DBInteraction import *
from tkinter import *

class cleanByArt():
    def __init__(self, frame, selectedPlaylist, auth):
        global authItems
        global db
        db = dbInteraction()
        authItems = auth
        self.clearFrame(frame)
        if selectedPlaylist['Playlist Name'] == 'Liked Playlist':
            data = self.getDataFromLiked()
        else:
            data = self.getDataFromOther(selectedPlaylist)
        holdResponses = data['holdResponses']
        data = data['data']
        length = len(data)
        frame.update()
        width = frame.winfo_width()
        lb = Listbox(frame, selectmode=MULTIPLE, height=int(length / 10), width=int(width / 20))
        confirm = Button(frame, text='Confirm', command=lambda: self.confirm(frame, lb, data, selectedPlaylist, holdResponses))
        sb = Scrollbar(frame, orient='vertical')
        sb.config(command=lb.yview)

        lb.config(yscrollcommand=sb.set)
        for i in data:
            name = i['artistName']
            trackCount = len(i['artistTracks'])
            add = f'{name} {trackCount}'
            lb.insert(END, add)
        confirm.pack(side='bottom')
        lb.pack(side='left')
        sb.pack(fill='y', side='right')

    def confirm(self, frame, lb, data, playlist, holdData):
        selected = lb.curselection()
        selected = [lb.get(i) for i in selected]
        self.clearFrame(frame)
        #Load current version of playlist into firebase
        #Delete Tracks from Playlist
        userId = self.getUserId()
        db.addUserPlaylist(userId, playlist, holdData)
        for i in selected:
            name = i[0:int(i.rfind(' '))]
            self.deleteFromLiked(name, data)
            
    def deleteFromLiked(self, artistName, data):
        for i in data:
            if i['artistName'] == artistName:
                artistId = i['artistId']
                artistTracks = i['artistTracks']
                artistTrackIds = i['artistTrackIds']
                break
        header = {
            'Authorization': authItems['type'] + ' ' + authItems['accessTok'],
            'Content-Type': 'application/json'
        }
        url = 'https://api.spotify.com/v1/me/tracks?ids='
        ids = []
        for i in artistTrackIds:
            url = url + i + ','
            ids.append(i)
            if len(ids) >= 20:
                url = url[:-1]
                data1 = json.dumps({'ids': ids})
                r = requests.delete(url=url, headers=header, data=data1)
                ids = []
                url = 'https://api.spotify.com/v1/me/tracks?ids='
        url = url[:-1]
        data1 = json.dumps({'ids': ids})
        r = requests.delete(url=url, headers=header, data=data1)
        ids = []
        url = 'https://api.spotify.com/v1/me/tracks?ids='

    def getDataFromOther(self, playlistInfo):
        playlistId = playlistInfo['Playlist Id']
        url = f'https://api.spotify.com/v1/playlists/{playlistId}'
        header = {
            'Authorization': authItems['type'] + ' ' + authItems['accessTok']
        }

        r = requests.get(url=url, headers=header)
        x = json.loads(r.text)
        next = x['tracks']['next']
        holdResponses = '{\n\"data\": [\n'
        while next != None:
            holdResponses = holdResponses + '\t' + r.text + ',\n'
            url = next
            r = requests.get(url=url, headers=header)
            x = json.loads(r.text)
            next = x['tracks']['next']
        holdResponses = holdResponses + '\t' + r.text
        holdResponses = holdResponses + '\n]\n}'
        x = json.loads(holdResponses)

        data = x['data']
        info = []
        trackArtists = []
        varArtCount = 1

        for i in data:
            items = i['tracks']['items']
            for j in items:
                arts = j['track']['artists']
                for k in arts:
                    artistName = k['name']
                    if artistName not in trackArtists:
                        if artistName == '':
                            artistName = f'Various Artists {varArtCount}'
                            varArtCount = varArtCount + 1
                        artistId = k['id']
                        hold = self.getArtTracks(data, artistName, False)
                        artistInfo = {
                            'artistName': artistName,
                            'artistId': artistId,
                            'artistTracks': hold['artistTracks'],
                            'artistTrackIds': hold['artistTrackIds']
                        }
                        info.append(artistInfo)
                        trackArtists.append(artistName)
        return {
            'data': info,
            'holdResponses': holdResponses
        }

    def getDataFromLiked(self):
        url = 'https://api.spotify.com/v1/me/tracks?limit=50'
        header = {
            'Authorization': authItems['type'] + ' ' + authItems['accessTok']
        }

        r = requests.get(url=url, headers=header)
        x = json.loads(r.text)
        next = x['next']
        
        dataFromLiked = '{\n\"data\": [\n'
        while next != None:
            dataFromLiked = dataFromLiked + '\t' + r.text + ',\n'
            url = next
            r = requests.get(url=url, headers=header)
            x = json.loads(r.text)
            next = x['next']
        dataFromLiked = dataFromLiked + '\t' + r.text
        dataFromLiked = dataFromLiked + ']\n}'
        
        x = json.loads(dataFromLiked)

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
                        hold = self.getArtTracks(data, artistName, True)
                        artistInfo = {
                            'artistName': artistName,
                            'artistId': artistId,
                            'artistTracks': hold['artistTracks'],
                            'artistTrackIds': hold['artistTrackIds']
                        }
                        info.append(artistInfo)
                        trackArtists.append(artistName)
        return {
            'data': info,
            'holdResponses': dataFromLiked
        }

    def getArtTracks(self, data, artistName, isLiked):
        tracks = []
        trackIds = []
        for i in data:
            if isLiked:
                items = i['items']
            else:
                items = i['tracks']['items']
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
    
    def clearFrame(self, frame):
        for i in frame.winfo_children():
            i.destroy()