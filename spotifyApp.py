from tkinter import *
import random
import string
import webbrowser
import base64
import json
import requests

authItems = {}

class start():
    def __init__(self, frame):
        b = Button(frame, text='Click to Start', command=lambda: self.startProgram(b))
        b.pack()
    def startProgram(self, start):
        c = 'bf9fd0131e0a4c56ab5ec69dc87befc3'
        s = '9ab7c1a94f2841d6bb97102680edd97d'
        redirect = 'http://localhost:80'
        chars = string.ascii_lowercase + string.digits
        state = ''.join(random.choice(chars) for i in range(16))
        scope = 'user-read-private,user-read-email'
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
        authItems = {
            'accessTok': x['access_token'],
            'type': x['token_type'],
            'expires_in': x['expires_in'],
            'refreshTok': x['refresh_token'],
            'scope': x['scope']
        }
        con.pickPage('Main', frame)

class MainScreen():
    def __init__(self, frame):
        global a
        global b
        a = Button(frame, text='Idk man, Im just vibin', command=self.check)
        a.pack()
        b = Button(frame, text='Quit', command=lambda: self.pickPage('Quit'))
        b.pack()
    def pickPage(self, page):
        a.destroy()
        b.destroy()
        con.pickPage(page, frame)
    def check(self):
        print('Hello')

class Quit():
    def __init__(self, frame):
        l = Label(frame, text='Are you sure?')
        yes = Button(frame, text='Yes', command=root.quit)
        no = Button(frame, text='No', command=frame)
        l.pack()
        yes.pack()
        no.pack()

class Controller():
    global frame
    def pickPage(self, page, frame):
        if page == 'Start':
            start(frame)
        elif page == 'Main':
            root.title('Main')
            m = MainScreen(frame)
        elif page == 'Quit':
            root.title('Quit')
            Quit(frame)
            print(authItems)
root = Tk()
root.title('Start')
con = Controller()
frame = Frame(root)
frame.pack()
con.pickPage('Start', frame)
root.mainloop()
