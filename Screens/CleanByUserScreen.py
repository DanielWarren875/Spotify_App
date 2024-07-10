from tkinter import *
import requests
from DBInteraction import *

class cleanByUser():
    def __init__(self, frame, playlist, auth):
        global authItems
        global db

        db = dbInteraction()
        authItems = auth
        self.clearFrame(frame)
            
        data = self.getData(playlist)
        print(data)
        frame.update()
        width = frame.winfo_width()
        length = frame.winfo_height()
        lb = Listbox(frame, selectmode=MULTIPLE, height=int(length / 10), width=int(width / 5))
        
        sb = Scrollbar(frame, orient='vertical')
        sb.config(command=lb.yview)

        lb.config(yscrollcommand=sb.set)
        ids = []
        uris = []
        for i in data:
            add = i['trackName'] + '\t\t\t'
            for j in i['artists']:
                add = add + j + '\t\t\t'
            add = add + i['albumName'] + '\t\t\t' + i['dateAdded']
            hold = i['trackId']
            ids.append(hold)
            hold = i['trackUri']
            uris.append(hold)
            lb.insert(END, add)

        confirm = Button(frame, text='Confirm', command=lambda: self.confirm(data, lb, playlist, frame, ids, uris))
        confirm.pack(side='bottom')
        lb.pack(side='left')
        sb.pack(fill='y', side='right')

    def confirm(self, data, lb, playlist, frame, ids, uris):
        selected = lb.curselection()

        deleteIds = []
        tracks = []
        for i in selected:
            deleteIds.append(ids[i])
            hold = {
                'uri': uris[i]
            }
            tracks.append(hold)

        self.clearFrame(frame)
        
        
        header = {
            'Authorization': authItems['type'] + ' ' + authItems['accessTok'],
            'Content-Type': 'application/json'
        }
        
        if playlist['Playlist Name'] == 'Liked Playlist':
            url = 'https://api.spotify.com/v1/me/tracks?ids='
            for i in deleteIds:
                url = url + i + ','
            url = url[:-1]
            data = json.dumps({'ids': deleteIds})
            r = requests.delete(url=url, headers=header, data=data)
        else:
            url = 'https://api.spotify.com/v1/playlists/' + playlist['Playlist Id'] + '/tracks'
            data = {
                'tracks': tracks,
                'snapshot_id': playlist['snapshot_id']
            }
            data = json.dumps(data)
            r = requests.delete(url=url, headers=header, data=data)
            print(r.text)





    def getData(self, playlist):
        header = {
            'Authorization': authItems['type'] + ' ' + authItems['accessTok']
        }
        data = []
        if playlist['Playlist Name'] == 'Liked Playlist':
            url = 'https://api.spotify.com/v1/me/tracks?limit=50'  
        else:
            url = 'https://api.spotify.com/v1/playlists/' + playlist['Playlist Id'] + '/tracks'
        
        while url != None:
                r = requests.get(url=url, headers=header)
                x = json.loads(r.text)
                next = x['next']
                items = x['items']
                for i in items:
                    dateAdded = i['added_at']
                    trackName = i['track']['name']
                    trackId = i['track']['id']
                    trackUri = i['track']['uri']
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
                        'dateAdded': dateAdded,
                        'trackUri': trackUri
                    }
                    data.append(info)
                url = next
        '''
        data = {
            'trackName': '',
            'trackId': '',
            'artists': [''],
            'albumName': '',
            'dateAdded': ''
        }
        '''
        
        return data

    def clearFrame(self, frame):
        for i in frame.winfo_children():
            i.destroy()