from tkinter import *
from Controller import *

class MainScreen():
    def __init__(self, frame, con, root):
        cleanPlayDate = Button(frame, text='Clean a Playlist By Date', command=lambda: con.pickPage(root, 'cleanPlayDate', frame))
        cleanPlayArt = Button(frame, text='Clean a Playlist By Artist', command=lambda: con.pickPage(root, 'cleanPlayArt', frame))
        cleanPlayUser = Button(frame, text='Clean a Playlist By Tracks You Pick', command=lambda: con.pickPage(root, 'cleanPlayUser', frame))
        revertPlay = Button(frame, text='Revert your playlist to a previous version', command=lambda: con.pickPage(root, 'revert', frame))
        cleanPlayDate.pack()
        cleanPlayArt.pack()
        cleanPlayUser.pack()
        revertPlay.pack()