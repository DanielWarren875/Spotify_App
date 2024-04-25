import json
import requests
from tkinter import *
from DBInteraction import *
class cleanByArt():
    def __init__(self, frame, playlist, authItems):
        self.clearFrame(frame)
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
        url = 'https://api.spotify.com/v1/me'
        header = {
            'Authorization': authItems['type'] + ' ' + authItems['accessTok']
        }

        r = requests.get(url=url, headers=header)
        x = json.loads(r.text)
        userId = x['id']


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
                for j in holdArts:
                    hold = j['name']
                    arts.append(hold)
                    holdInfo = {
                        'TrackId': trackId,
                        'Artist': hold
                    }
                    trackIds.append(holdInfo)
            url = next
            r = requests.get(url=url, headers=header)
            x = json.loads(r.text)
            next = x['next']
        items = x['items']
        for i in items:
            holdArts = i['track']['artists']
            trackId = i['track']['id']
            for j in holdArts:
                hold = j['name']
                arts.append(hold)
                holdInfo = {
                        'TrackId': trackId,
                        'Artist': hold
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