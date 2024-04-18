from Screens.MainScreen import MainScreen
from Screens.startScreen import *
from Screens.MainScreen import *
from Screens.RevertScreen import *
from PlaylistPick import *
from Screens.QuitScreen import *
from Screens.startScreen import start
class Controller():
    def pickPage(self, root, page, frame, authItems):
        if page == 'Start':
            start(frame, self, root, authItems)
        elif page == 'Main':
            self.clearFrame(frame)
            root.title('Main')
            m = MainScreen(frame, self, root, authItems)
        elif page == 'cleanPlayDate':
            self.clearFrame(frame)
            back = Button(root, text='Back to Main', command=lambda: self.pickPage(root, 'Main', frame, authItems))
            back.pack()
            n = pickPlaylist(frame, page, root, authItems)
        elif page == 'cleanPlayArt':
            self.clearFrame(frame)
            back = Button(root, text='Back to Main', command=self.pickPage(root, 'Main', frame, authItems))
            #back.pack()
            n = pickPlaylist(root, page, root, authItems, con)
        elif page == 'cleanPlayUser':
            self.clearFrame(frame)
            back = Button(root, text='Back to Main', command=self.pickPage(root, 'Main', frame, authItems))
            #back.pack()
            n = pickPlaylist(root, page, root, authItems, con)
        elif page == 'revert':
            r = revertScreen()
            r.loadData(authItems)
        elif page == 'Quit':
            self.clearFrame(frame)
            root.title('Quit')
            back = Button(frame, text='Back to Main', command=self.pickPage(root, 'Main', frame, authItems))
            #back.pack()
            Quit(frame, root)
    def clearFrame(self, frame):
        for i in frame.winfo_children():
            i.destroy()