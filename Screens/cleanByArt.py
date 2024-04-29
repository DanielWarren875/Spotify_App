import json
import requests
from tkinter import *
from DBInteraction import *
class cleanByArt():
    def __init__(self, frame, playlist, authItems):
        self.clearFrame(frame)
        global db
        db = dbInteraction()
        if playlist['Playlist Name'] == 'Liked Playlist':
            self.clearLiked(frame, authItems)
    def clearLiked(self, frame, authItems):
        url = 'https://api.spotify.com/v1/me/tracks'
        header = {
            'Authorization': authItems['type'] + ' ' + authItems['accessTok']
        }
        hold = self.getArtsFromLiked(url, header)
        arts = hold['ArtistsW/Count']
        trackIds = hold['ArtistsW/TrackIds']
        
        userId = self.getUserId(authItems)
        playlistId = userId + 'Liked Playlist'
        playlistId = "".join(playlistId.split())
        self.checkForDups(trackIds)
        return
        print(trackIds)
        print(len(trackIds))
        return

        db.addPlaylistTracks(userId, playlistId, trackIds)

        length = len(arts)
        lb = Listbox(frame, selectmode=MULTIPLE, height=length, width=200)
        b = Button(frame, text='Confirm', command=lambda: self.selectFromLiked(frame, lb, trackIds, arts, authItems))
        for i in arts:
            name = i['Name']
            count = i['TrackCount']
            add = f'{name} {count}'
            lb.insert(END, add)
        b.pack()
        lb.pack()

    def selectFromLiked(self, frame, lb, trackIds, artInfo, authItems):
        selectList = lb.curselection()
        hold = [lb.get(i) for i in selectList]
        removeTrackIds = []
        artistsToRemove = []

        for i in hold:
            for j in artInfo:
                holdArt = j['Name']
                if holdArt in i:
                    artistsToRemove.append(holdArt)
        
        for j in trackIds:
            holdName = j['Artist']
            if holdName in artistsToRemove:
                removeTrackIds.append(j['TrackId'])
        self.getUserId(authItems)

    def getUserId(self, authItems):
        url = 'https://api.spotify.com/v1/me'
        header = {
            'Authorization': authItems['type'] + ' ' + authItems['accessTok']
        }

        r = requests.get(url=url, headers=header)
        x = json.loads(r.text)
        return x['id']

    def getArtsFromLiked(self, url, header):
        r = requests.get(url=url, headers=header)
        x = json.loads(r.text)
        next = x['next']
        arts = []
        trackIds = []
        while next != None:
            items = x['items']
            for i in items:
                holdArts = i['track']['artists']
                trackId = i['track']['id']
                trackName = i['track']['name']
                
                artNames = []
                for j in holdArts:
                    hold = j['name']
                    arts.append(hold)
                    artNames.append(hold)
                holdInfo = {
                    'TrackId': trackId,
                    'TrackName': trackName,
                    'Artist': artNames
                }
                trackIds.append(holdInfo)
            url = next
            r = requests.get(url=url, headers=header)
            x = json.loads(r.text)
            next = x['next']
        items = x['items']
        for i in items:
            items = x['items']
            for i in items:
                holdArts = i['track']['artists']
                trackId = i['track']['id']
                trackName = i['track']['name']
                artNames = []
                for j in holdArts:
                    hold = j['name']
                    arts.append(hold)
                    artNames.append(hold)
                holdInfo = {
                    'TrackId': trackId,
                    'TrackName': trackName,
                    'Artist': artNames
                }
                trackIds.append(holdInfo)

        arts1 = []
        hold = []
        for i in arts:
            if i not in hold:
                items = {
                    'Name': i,
                    'TrackCount': arts.count(i)
                }
                arts1.append(items)
                hold.append(i)
        ret = {
            'ArtistsW/Count': arts1,
            'ArtistsW/TrackIds': trackIds
        }
        return ret
    def clearFrame(self, frame):
        for i in frame.winfo_children():
            i.destroy()
    def checkForDups(self, trackIds):
        for i in trackIds:
            for j in trackIds:
                if i['TrackId'] == j['TrackId'] and i != j:
                    print(i)