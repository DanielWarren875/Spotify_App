from tkinter import *
from Screens.QuitScreen import Quit
from PlaylistPick import *
from Controller import *


root = Tk()
root.title('Start')
root.geometry('500x500')
con = Controller()
frame = Frame(root)
frame.pack()
con.pickPage(root, 'Start', frame, None)
root.mainloop()
