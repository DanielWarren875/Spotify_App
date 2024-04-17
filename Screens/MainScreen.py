from tkinter import *
from Controller import *

class MainScreen():
    def __init__(self, frame, con, root, authItems):
        cleanPlayDate = Button(frame, text='Clean a Playlist By Date', command=lambda: con.pickPage(root, 'cleanPlayDate', frame, authItems))
        cleanPlayArt = Button(frame, text='Clean a Playlist By Artist', command=lambda: con.pickPage(root, 'cleanPlayArt', frame, authItems))
        cleanPlayUser = Button(frame, text='Clean a Playlist By Tracks You Pick', command=lambda: con.pickPage(root, 'cleanPlayUser', frame, authItems))
        revertPlay = Button(frame, text='Revert your playlist to a previous version', command=lambda: con.pickPage(root, 'revert', frame, authItems))
        cleanPlayDate.pack()
        cleanPlayArt.pack()
        cleanPlayUser.pack()
        revertPlay.pack()