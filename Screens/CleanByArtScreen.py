import tkinter
import pandas
import requests
from io import StringIO
from DBInteraction import *

class cleanByArt():
    def __init__(self, frame, playlist, auth):
        global authItems
        authItems = auth
        x = self.getDataFromLiked()
        y = self.getArtistNamesAndIds(x)
        

    def getDataFromLiked(self):
        url = 'https://api.spotify.com/v1/me/tracks'
        header = {
            'Authorization': authItems['type'] + ' ' + authItems['accessTok']
        }

        r = requests.get(url=url, headers=header)
        x = json.loads(r.text)
        next = x['next']
        data = []

        while next != None:
            items = x['items']
            for i in items:
                trackName = i['track']['name']
                trackId = i['track']['id']
                holdArts = i['track']['artists']
                arts = []
                artIds = []
                for j in holdArts:
                    holdName = j['name']
                    holdId = j['id']
                    arts.append(holdName)
                    artIds.append(holdId)
                hold = {
                    'arts': arts,
                    'artIds': artIds,
                    'trackName': trackName,
                    'trackId': trackId
                }
                data.append(hold)
            url = next
            r = requests.get(url=url, headers=header)
            x = json.loads(r.text)
            next = x['next']

        items = x['items']
        for i in items:
            trackName = i['track']['name']
            trackId = i['track']['id']
            holdArts = i['track']['artists']
            arts = []
            artIds = []
            for j in holdArts:
                holdName = j['name']
                holdId = j['id']
                arts.append(holdName)
                artIds.append(holdId)
            hold = {
                'arts': arts,
                'artIds': artIds,
                'trackName': trackName,
                'trackId': trackId
            }
            data.append(hold)
        return data
    
    def getArtistNamesAndIds(self, data):
        artists = []
        ids = []
        for i in data:
            for j in range(0, len(i['arts'])):
                if i['arts'][j] not in artists:
                    artists.append(i['arts'][j])
                    holdId = i['artIds'][j]
                    ids.append(holdId)
        return {
            'artists': artists,
            'ids': ids
        }