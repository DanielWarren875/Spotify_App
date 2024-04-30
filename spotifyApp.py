from tkinter import *
from Controller import *
from authItems import *


root = Tk()
root.title('Start')
root.geometry('1500x1500')
frame = Frame(root)
frame.pack()
a = authenticateItems()
con = Controller(root, frame, a)
con.pickPage(root, 'Start', frame, a)
root.mainloop()