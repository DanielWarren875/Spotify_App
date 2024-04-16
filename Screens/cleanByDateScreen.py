import datetime
import tkinter
import requests
import json
from tkinter import *

class cleanByDate():
    def __init__(self, frame, playlist, authItems):
        self.clearFrame(frame)
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
        earliest = datetime.datetime.now()
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
        earliest = trackInfo[len(trackInfo) - 1]['addedAt']
        latest = trackInfo[0]['addedAt']
        print(f'{earliest} {latest}')
        for i in range(2015, datetime.datetime.now().year + 1):
            years.append(i)
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        days = []
        for i in range(1, 32):
            days.append(i)

        self.clearFrame(frame)
        year = StringVar(frame)
        month = StringVar(frame)
        day = StringVar(frame)


        year.set(years[0])
        month.set(months[0])
        day.set(days[0])


        yearMenu = OptionMenu(frame, year, *years)
        monthMenu = OptionMenu(frame, month, *months)
        dayMenu = OptionMenu(frame, day, *days)
        yearMenu.config(bg="WHITE", fg="BLACK")
        yearMenu["menu"].config(bg="WHITE")
        monthMenu.config(bg="WHITE", fg="BLACK")
        monthMenu["menu"].config(bg="WHITE")
        dayMenu.config(bg="WHITE", fg="BLACK")
        dayMenu["menu"].config(bg="WHITE")
        monthMenu.pack()
        dayMenu.pack()
        yearMenu.pack()

        vals = {
            'Year': year,
            'Month': month,
            'Day': day
        }

        confirm = Button(frame, text='Confirm Deletion Date', command=lambda: self.confirm(frame, vals))
        confirm.pack()



    def clearFrame(self, frame):
        for i in frame.winfo_children():
            i.destroy()
    def confirm(self, frame, vals):
        year = vals['Year'].get()
        month = vals['Month'].get()
        day = vals['Day'].get()
        monthsWithMoreDays = ['Jan', 'Mar', 'May', 'Jul', 'Aug', 'Oct', 'Dec']
        global isValid
        if month == 'Feb' and int(day) > 28 and int(year) % 4 != 0:
            b = Label(frame, text='Invalid Date, Please Try Again')
            b.pack()
            isValid = False
        elif month not in monthsWithMoreDays and int(day) == 31:
            b = Label(frame, text='Invalid Date, Please Try Again')
            b.pack()
            isValid = False
        else:
            isValid = True
        vals = {
            'yearVal': year,
            'monthVal': month,
            'dayVal': day
        }

        if isValid:
            self.clearFrame(frame)
            self.clearLikedPlaylist(frame, vals)
    
    def clearLikedPlaylist(self, frame, date):
        print(date)

        
        