from Screens.MainScreen import MainScreen
from Screens.startScreen import *
from Screens.MainScreen import *
from Screens.RevertScreen import *
from PlaylistPick import *
from Screens.QuitScreen import *
from Screens.startScreen import start
class Controller():
    def __init__(self, root, frame, authItems):
        global back
        back = Button(root, text='Back to Main', command=lambda: self.pickPage(root, 'Main', frame, authItems))
    def pickPage(self, root, page, frame, authItems):
        self.clearFrame(frame)
        if page == 'Start':
            start(frame, self, root, authItems)
        elif page == 'Main':
            self.clearFrame(frame)
            root.title('Main')
            back.grid_remove()
            m = MainScreen(frame, self, root, authItems)
        elif page == 'cleanPlayDate':
            self.clearFrame(frame)
            back.grid(row=1, column=1)
            n = pickPlaylist(frame, page, root, authItems)
        elif page == 'cleanPlayArt':
            self.clearFrame(frame)
            back.grid(row=0, column=1)
            n = pickPlaylist(frame, page, root, authItems)
        elif page == 'cleanPlayUser':
            self.clearFrame(frame)
            back.grid(row=1, column=0)
            n = pickPlaylist(frame, page, root, authItems)
        elif page == 'revert':
            self.clearFrame(frame)
            back.grid(row=1, column=0)
            n = pickPlaylist(frame, page, root, authItems)
        elif page == 'Quit':
            self.clearFrame(frame)
            root.title('Quit')
            back.grid(row=1, column=0)
            Quit(frame, root)

    def clearFrame(self, frame):
        for i in frame.winfo_children():
            i.destroy()