from tkinter import *
import requests
import json
from Screens.cleanByDateScreen import *
userId = ''
class pickPlaylist():
    def __init__(self, frame, nextPage, root, auth):
        global userId
        global authItems
        authItems = auth
        root.title('Pick a Playlist')
        if userId == '':
            userId = self.getUserId()
        playlists = self.getUserPlaylists()
        length = len(playlists)
        lb = Listbox(frame, selectmode=SINGLE, height=length)
        for i in playlists:
            name = i['Playlist Name']
            owner = i['Owner']
            count = i['Track Count']
            add = f'{name} {owner} {count}'
            lb.insert(END, add)
        lb.pack()
        back = Button(frame, text='Back', command=lambda: self.back())
        b = Button(frame, text='Confirm', command=lambda: self.select(root, frame, nextPage, lb, playlists))
        b.pack()
    def back(self, frame):
        print('Yes')
    def select(self, root, frame, nextPage, lb, playlists):
        selected = lb.curselection()
        hold = [lb.get(i) for i in selected]

        for j in playlists:
            if j['Playlist Name'] in hold[0]:
                playlist = j
                break
        if nextPage == 'cleanPlayDate':
            root.title('Clean Playlist By Date')
            n = cleanByDate(frame, playlist, authItems)


    def getUserPlaylists(self):
        url = f'https://api.spotify.com/v1/me/playlists'
        header = {
            'Authorization': authItems['type'] + ' ' + authItems['accessTok']
        }
        r = requests.get(url=url, headers=header)
        print(r.text)
        x = json.loads(r.text)
        next = x['next']
        ownerPlay = []
        ownerPlay.append(self.getLikedPlaylistInfo())
        #otherPlay = []
        
        while next != None:
            url = next
            items = x['items']
            
            for i in items:
                owner = i['owner']['id']
                name = i['name']
                playId = i['id']
                snapshot = i['snapshot_id']
                length = i['tracks']['total']
                hold = {
                    'Owner': owner,
                    'Playlist Name': name,
                    'Playlist Id': playId,
                    'snapshot_id': snapshot,
                    'Track Count': length
                }
                if owner == userId:
                    ownerPlay.append(hold)
                #else:
                    #otherPlay.append(hold)
            r = requests.get(url=url, headers=header)
            x = json.loads(r.text)
            next = x['next']
        '''return {
            'User Owned': ownerPlay,
            'Other Owned': otherPlay
        }'''
        return ownerPlay

    def getLikedPlaylistInfo(self):
        url = 'https://api.spotify.com/v1/me/tracks'
        header = {
            'Authorization': authItems['type'] + ' ' + authItems['accessTok']
        }
        r = requests.get(url=url, headers=header)
        x = json.loads(r.text)
        return {
            'Owner': userId,
            'Playlist Name': 'Liked Playlist',
            'Playlist Id': 'me',
            'snapshot_id': 'None',
            'Track Count': x['total']
        }

    def getUserId(self):
        url = 'https://api.spotify.com/v1/me'
        header = {
            'Authorization': authItems['type'] + ' ' + authItems['accessTok']
        }
        r = requests.get(url=url, headers=header)
        x = json.loads(r.text)
        return x['id']