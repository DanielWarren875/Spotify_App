from Screens.MainScreen import MainScreen
from Screens.startScreen import *
from Screens.MainScreen import *
from Screens.RevertScreen import *
from PlaylistPick import *
from Screens.QuitScreen import *

class Controller():
    global frame
    

    def pickPage(self, root, page, frame, authItems):
        if page == 'Start':
            start(frame, self, root)
        elif page == 'Main':
            if back.winfo_exists():
                back.destroy()
            self.clearFrame(frame)
            root.title('Main')
            m = MainScreen(frame, self, root)
        elif page == 'cleanPlayDate':
            
            self.clearFrame(frame)
            back.pack()
            n = pickPlaylist(frame, page, root, authItems, con)
        elif page == 'cleanPlayArt':
            self.clearFrame(frame)
            back = Button(frame, text='Back to Main', command=self.pickPage(root, 'Main', frame, authItems))
            back.pack()
            n = pickPlaylist(frame, page, root, authItems, con)
        elif page == 'cleanPlayUser':
            self.clearFrame(frame)
            back = Button(frame, text='Back to Main', command=self.pickPage(root, 'Main', frame, authItems))
            back.pack()
            n = pickPlaylist(frame, page, root, authItems, con)
        elif page == 'revert':
            self.clearFrame(frame)
            #n = revert()
            back = Button(frame, text='Back to Main', command=self.pickPage(root, 'Main', frame, authItems))
            back.pack()
            self.pickPage('Quit', frame)
        elif page == 'Quit':
            self.clearFrame(frame)
            root.title('Quit')
            back = Button(frame, text='Back to Main', command=self.pickPage(root, 'Main', frame, authItems))
            back.pack()
            Quit(frame, root)
            print(authItems)
    def clearFrame(self, frame):
        for i in frame.winfo_children():
            i.destroy()
