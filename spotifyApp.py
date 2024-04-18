from tkinter import *
from Screens.QuitScreen import Quit
from PlaylistPick import *
from Controller import *
from authItems import *
from Screens.RevertScreen import *


root = Tk()
root.title('Start')
root.geometry('500x500')
frame = Frame(root)
frame.pack()
con = Controller()
a = authenticateItems()
con.pickPage(root, 'Start', frame, a)
root.mainloop()