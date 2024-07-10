from tkinter import *
from Controller import *
from authItems import *


root = Tk()
root.title('Start')
root.geometry('750x750')
frame = Frame(root)
frame.grid(row=0, column=0, columnspan=5)
a = authenticateItems() 
con = Controller(root, frame, a)
con.pickPage(root, 'Start', frame, a)
root.mainloop()