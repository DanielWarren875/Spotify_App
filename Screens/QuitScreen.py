from tkinter import *
class Quit():
    def __init__(self, frame, root):
        root.title('Quit')
        l = Label(frame, text='Are you sure?')
        yes = Button(frame, text='Yes', command=root.quit)
        no = Button(frame, text='No', command=frame)
        l.pack()
        yes.pack()
        no.pack()