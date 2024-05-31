from tkinter import *
import requests
class search():
    def __init__(self, frame, root, auth, con):
        auth = auth.getAuthItems()
        self.init(frame, root, auth, con)

    def init(self, frame, root, auth, con):
        e = Entry(frame, text='Enter you search request here')
        
        l = Label(frame, text='Search Type')
        lb = Listbox(frame, selectmode=MULTIPLE, height=20, width=20)
        b = Button(frame, text='Confirm', command=lambda: self.confirm(frame, root, auth, con, e, b, lb))
        lb.insert(END, 'album')
        lb.insert(END, 'artist')
        lb.insert(END, 'track')

        e.grid(row=0, column=0, columnspan=1)
        l.grid(row=1, column=0, columnspan=1)
        lb.grid(row=2, column=0, columnspan=1)
        b.grid(row=3, column=0, columnspan=1)
    
    def confirm(self, frame, root, auth, con, e, b, searchTypes):
        height = int(frame.winfo_height() / 2)
        width = int(frame.winfo_width() / 10)
        lb = Listbox(frame, selectmode=MULTIPLE, height=height, width=width)
        selected = searchTypes.curselection()
        if len(selected) == 0:
            self.errorType(frame, root, auth, con)
        selected = [searchTypes.get(i) for i in selected]
        searchType = ''
        for i in selected:
            searchType = searchType + i + '%2C'
        searchType = searchType[:-3]

        q = e.get()
        if len(q) == 0:
            self.errorQuery(frame, root, auth, con)
        q = q.replace(' ', '+')
        url = f'https://api.spotify.com/v1/search?q={q}&type={searchType}'
        header = {
            'Authorization': auth['type'] + ' ' + auth['accessTok'],
        }
        r = requests.get(url=url, headers=header)
        print(r.text)
    
    def errorType(self, frame, root, auth, con):
        self.clearFrame(frame)
        l = Label(frame, text='Please select at least one search type').grid(row=5, column=0)
        self.init(frame, root, auth, con)

    def errorQuery(self, frame, root, auth, con):
        self.clearFrame(frame)
        l = Label(frame, text='Please Enter a Search Request').grid(row=5, column=0)
        self.init(frame, root, auth, con)

    def clearFrame(self, frame):
        for i in frame.winfo_children():
            i.destroy()