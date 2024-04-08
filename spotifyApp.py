import base64
from tkinter import *
import webbrowser

root = Tk()

def getAuthCode():
    def getFromTextBar():
        hold = e.get()
        print(hold)
        i = hold.index('code=') + 5
        j = hold.index('&')
        code = hold[i:j]
        
        encode = base64.urlsafe_b64encode((c + ':' + s).encode())
        headers = {
            'Authorization': 
        }
        

    global authItems
    c = "bf9fd0131e0a4c56ab5ec69dc87befc3"
    s = "9ab7c1a94f2841d6bb97102680edd97d"
    redirect = "http://localhost:80"
    scope = "user-read-private,user-library-read,user-library-modify,user-modify-playback-state,user-read-playback-state"
    uri = "https://accounts.spotify.com/api/token"
    URL = "https://accounts.spotify.com/authorize?client_id=" 
    URL += c + "&response_type=code&redirect_uri=" + redirect +"&state=abcdefghijklmnop&scope=" + scope
    webbrowser.open(URL)

    start.destroy()
    e = Entry(root, width=100)
    e.pack()
    e.insert(0, 'Paste contents from Address Bar Here')
    b = Button(root, text='Confirm', command=getFromTextBar)
    b.pack()

start = Button(root, text='Click to Start', command=getAuthCode)
start.pack()
root.mainloop()
