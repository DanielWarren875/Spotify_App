from tkinter import *
from PyQt5.QtWidgets import QApplication
import random
import string
import webbrowser
import base64

import requests
root = Tk()
page = 'Start'

def getAuthCode():
    def getCode():
        hold = e.get()
        i = hold.find('code=')
        j = hold.find('&')
        code = hold[i + 5: j]
        print(hold + '\n' + code)
        e.destroy()
        b.destroy()
        getAuthItems(code)

    def getAuthItems(code):
        body = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect
        }

        headers = {
            'Authorization': 'Basic ' + encode,
            'content-type': 'application/x-www-form-urlencoded'
        }
        url = 'https://accounts.spotify.com/api/token'
        r = requests.post(url=url, headers=headers, params=body)
        print(r.text)

    global authItems
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
    encode = base64.b64encode(f'{c}:{s}')
    start.destroy()
    e = Entry(root, text='Paste Address Here')
    b = Button(root, text='Confirm', command=getCode)
    e.pack()
    b.pack()


start = Button(root, text='Click to Start', command=getAuthCode)
start.pack()

root.mainloop()
