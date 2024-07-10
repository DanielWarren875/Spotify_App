from tkinter import *
from Controller import *
from authItems import *

#Create, size, and title root window
root = Tk()
root.title('Start')
root.geometry('750x750')

#Create Frame and place it in root
frame = Frame(root)
frame.grid(row=0, column=0, columnspan=5)

#Create and initialize authenticateItems and Controller objects
a = authenticateItems() 
con = Controller(root, frame, a)
#Go to Start Page which handles the spotify authentication process
con.pickPage(root, 'Start', frame, a)
root.mainloop()