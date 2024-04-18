import json
import MySQLdb
import requests
from tkinter import *
from DBInteraction import *
class revertScreen(): 
    def __init__(self, frame, auth, selectedPlaylist):
        self.clearFrame(frame)
        db = dbInteraction()
        userId = auth['userId']
        x = db.getPlaylistInfo(userId, selectedPlaylist)

        print(x)
    def clearFrame(self, frame):
        for i in frame.winfo_children():
            i.destroy()
