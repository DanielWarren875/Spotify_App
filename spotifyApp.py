import datetime
import os
import time
from tkinter import *
import random
import string
import webbrowser
import base64
import json
import requests
from Screens.QuitScreen import Quit
from PlaylistPick import *

authItems = {}
userId = ''

class start():
    def __init__(self, frame):
        b = Button(frame, text='Click to Start', command=lambda: self.startProgram(b))
        b.pack()
    def startProgram(self, start):
        global authItems
        f = open('AuthItems.json', 'r')
        if os.stat('/Users/danielwarren/Desktop/Spotify_App/AuthItems.json').st_size != 0:
            x = json.load(f)
            a = x['Expire_Time']
            check = datetime.datetime.strptime(a, '%Y-%m-%d %H:%M:%S.%f')
            if datetime.datetime.now() < check:
                authItems = {
                    'accessTok': x['accessTok'],
                    'type': x['type'],
                    'expires_in': x['expires_in'],
                    'refreshTok': x['refreshTok'],
                    'scope': x['scope'], 
                    'Access_Time': x['Access_Time'],
                    'Expire_Time': x['Expire_Time']
                }
                con.pickPage('Main', frame)
                return
        c = 'bf9fd0131e0a4c56ab5ec69dc87befc3'
        s = '9ab7c1a94f2841d6bb97102680edd97d'
        redirect = 'http://localhost:80'
        chars = string.ascii_lowercase + string.digits
        state = ''.join(random.choice(chars) for i in range(16))
        scope = 'user-read-private,user-read-email,playlist-read-private,user-library-read'
        type = 'code'
        url = f'http://accounts.spotify.com/authorize?response_type={type}'
        url = url + f'&client_id={c}&scope={scope}'
        url = url + f'&redirect_uri={redirect}&state={state}'
        webbrowser.open(url)
        global encode
        encode = base64.urlsafe_b64encode((c + ':' + s).encode())
        start.destroy()
        e = Entry(frame, text='Paste Address Here')
        b = Button(frame, text='Confirm', command=lambda: self.getCode(e, b))
        e.pack()
        b.pack()
        
    def getCode(self, e, b):
        hold = e.get()
        i = hold.find('code=')
        j = hold.find('&')
        code = hold[i + 5: j]
        e.destroy()
        b.destroy()
        self.getAuthItems(code)

    def getAuthItems(self, code):
        global authItems
        body = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': 'http://localhost:80'
        }

        headers = {
            "Authorization": 'Basic %s' %encode.decode('ascii'),
            'content-type': 'application/x-www-form-urlencoded'
        }
        url = 'https://accounts.spotify.com/api/token'
        r = requests.post(url=url, headers=headers, params=body)
        x = json.loads(r.text)
        now = datetime.datetime.now()
        expTime = str(now + datetime.timedelta(seconds=3600))
        now = str(now)
        authItems = {
            'accessTok': x['access_token'],
            'type': x['token_type'],
            'expires_in': x['expires_in'],
            'refreshTok': x['refresh_token'],
            'scope': x['scope'], 
            'Access_Time': now,
            'Expire_Time': expTime
        }

        f = open('AuthItems.json', 'w')
        json.dump(authItems, f, indent=4)
        con.pickPage('Main', frame)


class MainScreen():
    def __init__(self, frame):
        cleanPlayDate = Button(frame, text='Clean a Playlist By Date', command=lambda: con.pickPage('cleanPlayDate', frame))
        cleanPlayArt = Button(frame, text='Clean a Playlist By Artist', command=lambda: con.pickPage('cleanPlayArt', frame))
        cleanPlayUser = Button(frame, text='Clean a Playlist By Tracks You Pick', command=lambda: con.pickPage('cleanPlayUser', frame))
        revertPlay = Button(frame, text='Revert your playlist to a previous version', command=lambda: con.pickPage('revert', frame))
        cleanPlayDate.pack()
        cleanPlayArt.pack()
        cleanPlayUser.pack()
        revertPlay.pack()

class Controller():
    global frame
    def pickPage(self, page, frame):
        if page == 'Start':
            start(frame)
        elif page == 'Main':
            self.clearFrame(frame)
            root.title('Main')
            m = MainScreen(frame)
        elif page == 'cleanPlayDate':
            self.clearFrame(frame)
            n = pickPlaylist(frame, page, root, authItems, con)
        elif page == 'cleanPlayArt':
            self.clearFrame(frame)
            n = pickPlaylist(frame, page, root, authItems, con)
        elif page == 'cleanPlayUser':
            self.clearFrame(frame)
            n = pickPlaylist(frame, page, root, authItems, con)
        elif page == 'revert':
            self.clearFrame(frame)
            #n = revert()
            self.pickPage('Quit', frame)
        elif page == 'Quit':
            self.clearFrame(frame)
            root.title('Quit')
            Quit(frame, root)
            print(authItems)
    def clearFrame(self, frame):
        for i in frame.winfo_children():
            i.destroy()
root = Tk()
root.title('Start')
root.geometry('500x500')
con = Controller()
frame = Frame(root)
frame.pack()
con.pickPage('Start', frame)
root.mainloop()
