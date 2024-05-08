from tkinter import *
from Controller import *
from authItems import * 
import base64
import random
import string
import requests
import datetime
import os
import json
import webbrowser
from DBInteraction import *


class start():
    def __init__(self, framer, controller, root1, authItems1):
        global frame
        global con
        global root
        global authItems
        authItems = authItems1
        frame = framer
        con = controller
        root = root1
        b = Button(frame, text='Click to Start', command=lambda: self.startProgram(b))
        b.pack()

    def startProgram(self, start):
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
                    'Expire_Time': x['Expire_Time'],
                    'UserId': x['UserId']
                }
                items = authenticateItems()
                items.setAuthItems(authItems)
                con.pickPage(root, 'Main', frame, items)
                return
        c = 'bf9fd0131e0a4c56ab5ec69dc87befc3'
        s = '9ab7c1a94f2841d6bb97102680edd97d'
        redirect = 'http://localhost:80'
        chars = string.ascii_lowercase + string.digits
        state = ''.join(random.choice(chars) for i in range(16))
        scope = 'user-read-private,user-read-email,playlist-read-private,user-library-read,playlist-read-collaborative,user-library-modify'
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
        url = 'https://api.spotify.com/v1/me'
        headers = {
            'Authorization': x['token_type'] + ' ' + x['access_token']
        }
        r = requests.get(url=url, headers=headers)
        y = json.loads(r.text)
        userId = y['id']
        authItems = {
            'accessTok': x['access_token'],
            'type': x['token_type'],
            'expires_in': x['expires_in'],
            'refreshTok': x['refresh_token'],
            'scope': x['scope'], 
            'Access_Time': now,
            'Expire_Time': expTime,
            'UserId': userId
        }
        a = authenticateItems()
        a.setAuthItems(items=authItems)
        f = open('AuthItems.json', 'w')
        json.dump(authItems, f, indent=4)

        db = dbInteraction()
        db.addUserToDB(userId)
        con.pickPage(root, 'Main', frame, a)

