from tkinter import *
from Controller import *
from authItems import *


root = Tk()
root.title('Start')
root.geometry('1500x1500')
frame = Frame(root)
frame.grid(row=1, column=0)
a = authenticateItems()
con = Controller(root, frame, a)
con.pickPage(root, 'Start', frame, a)
root.mainloop()