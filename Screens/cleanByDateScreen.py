import datetime
import tkinter
import requests
import json
from tkinter import *

class cleanByDate():
    def __init__(self, frame, playlist, authItems):
        if playlist['Playlist Name'] == 'Liked Playlist':
            self.likedPlaylist(frame, authItems)
    def likedPlaylist(self, frame, authItems):
        url = 'https://api.spotify.com/v1/me/tracks'
        header = {
            'Authorization': authItems['type'] + ' ' + authItems['accessTok']
        }
        trackInfo = []
        r = requests.get(url=url, headers=header)
        x = json.loads(r.text)
        next = x['next']

        while next != None:
            items = x['items']
            for i in items:
                trackName = i['track']['name']
                artists = i['track']['album']['artists']
                trackId = i['track']['id']
                addedAt = i['added_at']
                arts = []
                for j in artists:
                    hold = j['name']
                    arts.append(hold)
                info = {
                    'trackName': trackName,
                    'artists': arts,
                    'trackId': trackId,
                    'addedAt': addedAt
                }
                trackInfo.append(info)
            url = next
            r = requests.get(url=url, headers=header)
            x = json.loads(r.text)
            next = x['next']
        items = x['items']
        for i in items:
            trackName = i['track']['name']
            artists = i['track']['album']['artists']
            trackId = i['track']['id']
            addedAt = i['added_at']
            arts = []
            for j in artists:
                hold = j['name']
                arts.append(hold)
            info = {
                'trackName': trackName,
                'artists': arts,
                'trackId': trackId,
                'addedAt': addedAt
            }
            trackInfo.append(info)
        years = []
        for i in range(2015, datetime.datetime.now().year + 1):
            years.append(i)

        self.clearFrame(frame)
        variable = StringVar(frame)
        variable.set(years[0])

        w = OptionMenu(frame, variable, *years)
        w.pack()


    def clearFrame(self, frame):
        for i in frame.winfo_children():
            i.destroy()

        
        