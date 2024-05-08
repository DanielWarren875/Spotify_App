from tkinter import *
import requests
import json
from Screens.RevertScreen import *
from Screens.CleanByArtScreen import cleanByArt
from authItems import *
from DBInteraction import *
userId = ''
class pickPlaylist():
    def __init__(self, frame, nextPage, root, auth):
        global userId
        global authItems
        authItems = auth.getAuthItems()
        root.title('Pick a Playlist')
        if userId == '':
            userId = self.getUserId()
        playlists = self.getUserPlaylists()

        db = dbInteraction()



        length = len(playlists)
        lb = Listbox(frame, selectmode=SINGLE, height=length, width=200)
        for i in playlists:
            name = i['Playlist Name']
            owner = i['Owner']
            count = i['Track Count']
            add = f'{name} {owner} {count}'
            lb.insert(END, add)
        lb.pack()
        
        b = Button(frame, text='Confirm', command=lambda: self.select(root, frame, nextPage, lb, playlists))
        b.pack()
    def select(self, root, frame, nextPage, lb, playlists):
        selected = lb.curselection()
        hold = [lb.get(i) for i in selected]
        print(nextPage)
        for j in playlists:
            if j['Playlist Name'] in hold[0]:
                playlist = j
                break
        if nextPage == 'cleanPlayArt':
            root.title('Clean Playlist By Artist')
            self.clearFrame(root)
            n = cleanByArt(frame, playlist, authItems)
        elif nextPage == 'revert':
            root.title('Revert Playlist to Previous Version')
            r = revertScreen(frame, authItems, playlist)


    def getUserPlaylists(self):
        url = f'https://api.spotify.com/v1/me/playlists'
        header = {
            'Authorization': authItems['type'] + ' ' + authItems['accessTok']
        }
        r = requests.get(url=url, headers=header)
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
    

    def clearFrame(self, root):
        for i in root.winfo_children():
            if isinstance(i, Frame):
                for j in i.winfo_children():
                    j.destroy()
            else:
                i.destroy()