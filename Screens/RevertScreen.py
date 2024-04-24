import json
import requests
from tkinter import *

class revertScreen(): 
    def __init__(self, frame, auth, selectedPlaylist):
        self.clearFrame(frame)
        userId = auth['userId']
    def clearFrame(self, frame):
        for i in frame.winfo_children():
            i.destroy()
