import json
import requests
from tkinter import *

from DBInteraction import dbInteraction

class revertScreen():
    def __init__(self, frame, auth, selectedPlaylist):
        global authItems
        global db
        global userId
        global playlistName
        db = dbInteraction()
        authItems = auth
        self.clearFrame(frame)
        userId = authItems['UserId']
        playlistName = selectedPlaylist['Playlist Name']
        self.init(frame)

    def init(self, frame):
        data = db.getPlaylistVersionData(userId, playlistName)
        
        if data == None:
            l = Label(frame, text=f'{playlistName} does not have any previous versions')
            l.pack()
        else:
            length = len(data)
            l = Label(frame, text='Version Id\tDate Added\tTrack Count')
            lb = Listbox(frame, selectmode=SINGLE, height=length, width=200)
            for i in data:
                id = i['versionId']
                dateAdded = i['dateAdded']
                trackCount = i['trackCount']
                add = f'{id}\t{dateAdded}\t{trackCount}'
                lb.insert(END, add)
            
            l.pack()
            lb.pack()

            view = Button(frame, text='View Tracks within selected version', command=lambda:self.viewTracks(frame, lb, data))
            confirm = Button(frame, text='Confirm', command=lambda:self.confirmSelection(frame, lb, data))
            view.pack()
            confirm.pack()

    def viewTracks(self, frame, lb, data):
        hold = lb.curselection()
        selected = [lb.get(i) for i in hold]
        selected = selected[0]
        for i in data:
            if i['versionId'] in selected:
                version = i
                break
        self.clearFrame(frame)
        back = Button(frame, text='Select different verison', command=lambda:self.backToPlayVerSelect(frame, selected))
        back.pack()
        l = Label(frame, text=selected)
        l.pack()
        lb = Listbox(frame, selectmode=None, height=len(version['trackRefs']), width=200)
        for i in version['trackRefs']:
            info = db.getTrackInfo(i.id)
            hold = info['trackName'] + '\t' + info['artists']
            lb.insert(END, hold)
        lb.pack()

    def backToPlayVerSelect(self, frame, selected):
        self.clearFrame(frame)
        self.init(frame, authItems, selected)

    def confirmSelection(self, frame, lb, data):
        hold = lb.curselection()
        selected = [lb.get(i) for i in hold]
        selected = selected[0]
        for i in data:
            if i['versionId'] in selected:
                version = i
                break
        self.clearFrame(frame)
        l = Label(frame, text='Would you like to keep the songs that are in the playlist but not in this version?')
        yes = Button(frame, text='Yes', command=None)
        no = Button(frame, text='No', command=lambda:self.delete(frame, version))
        l.pack()
        yes.pack()
        no.pack()

    def delete(self, frame, version):
        self.clearFrame(frame)
        ids = []
        for i in version['trackRefs']:
            ids.append(i.id)
        if userId in version['versionId'] and 'LikedPlaylist' in version['versionId']:
            url = 'https://api.spotify.com/v1/me/tracks'
            header = {
                'Authorization': authItems['type'] + ' ' + authItems['accessTok']
            }
            r = requests.get(url=url, headers=header)
            x = json.loads(r.text)
            next = x['next']
            apiIds = []
            while next != None:
                items = x['items']
                for i in items:
                    hold = i['track']['id']
                    apiIds.append(hold)
                url = next
                r = requests.get(url=url, headers=header)
                x = json.loads(r.text)
                next = x['next']
            items = x['items']
            for i in items:
                hold = i['track']['id']
                apiIds.append(hold)
            
            while len(apiIds) > 0:
                if len(apiIds) > 50:
                    delete = apiIds[0:50]
                    apiIds = apiIds[50:]
                else:
                    delete = apiIds
                    apiIds = []
                header = {
                    'Authorization': authItems['type'] + ' ' + authItems['accessTok'],
                    'Content-Type': 'application/json'
                }
                
                url = 'https://api.spotify.com/v1/me/tracks?ids='
                for i in delete:
                    url = url + i + ','
                url = url[:-1]
                deleteData = json.dumps({'ids': delete})
                r = requests.delete(url=url, headers=header, data=deleteData)

            while len(ids) > 0:
                if len(ids) > 50:
                    add = ids[0:50]
                    ids = ids[50:]
                else:
                    add = ids
                    ids = []
                url = 'https://api.spotify.com/v1/me/tracks?ids='
                for i in add:
                    url = url + i + ','
                url = url[:-1]
                addData = json.dumps({'ids': add})
                r = requests.put(url=url, headers=header, data=addData)
            
    def clearFrame(self, frame):
        for i in frame.winfo_children():
            i.destroy()
