from cmath import sqrt
from tkinter import *
from firestoreInteraction import *
from apiInteraction import *
from uuid import getnode as get_mac
class signIn():
	def __init__(self):
		mac = get_mac()
		x = f.checkForDevice(mac)
		if x == None:
			self.signInScreen()
		else:
			global userData
			data = x['authData']
			userData = api.refreshToken(data)
			clearFrame(frame)
			mainMenu()
		
	def signInScreen(self):
		email = StringVar()
		password = StringVar()
		root.title('Sign In')
		title = Label(frame, text='Welcome, please sign in')
		title.grid(row=0, column=1, columnspan=3)
		Label(frame, text='Enter Email Address').grid(row=1, column=0, columnspan=3)
		Entry(frame, highlightbackground='Green', textvariable=email).grid(row=2, column=1, columnspan=3)
		Label(frame, text='Enter Password').grid(row=3, column=0, columnspan=3)
		Entry(frame, highlightbackground='Green', textvariable=password).grid(row=4, column=1, columnspan=3)
		signIn = Button(frame, text='Sign In', command=lambda:self.confirm(email, password)).grid(row=5, column=1, columnspan=3)
		global var
		var = IntVar()
		checkbutton = Checkbutton(frame, text="Remember Me?", variable=var,
                             onvalue=1, offvalue=0, command=lambda:rememberDevice(var))
		checkbutton.grid(row=6, column=1, columnspan=3)
		a = Label(frame, text='New User? Create an account here')
		a.bind("<Button-1>",lambda e: signUp())
		a.grid(row=7, column=1, columnspan=3)
		
		
	def checkData(self, email, password):
		email = email.get()
		password = password.get()
		global userData
		userData = f.retrieveAuthData(email, password)
		if isinstance(userData, str):
			print('Error')
			return 'Error'
		else:
			return userData
		
	def confirm(self, email, password):
		data = self.checkData(email, password)
		mac = rememberDevice(var)
		if isinstance(data, dict):
			global userData
			userData = api.refreshToken(data)
			
			if mac != None:
				f.rememberDevice(mac)
			clearFrame(frame)
			mainMenu()
		else:
			print('No')
			
class signUp():
	def __init__(self):
		email = StringVar()
		confirmEmail = StringVar()
		password = StringVar()
		confirmPass = StringVar()
		clearFrame(frame)
		root.title('Sign Up')
		Label(frame, text='Sign Up').grid(row=0, column=1, columnspan=3)
		Label(frame, text='Enter Your Email').grid(row=1, column=1, columnspan=3)
		Entry(frame, highlightbackground='Green', textvariable=email).grid(row=2, column=1, columnspan=3)
		Label(frame, text='Confirm Your Email').grid(row=3, column=1, columnspan=3)
		Entry(frame, highlightbackground='Green', textvariable=confirmEmail).grid(row=4, column=1, columnspan=3)
		Label(frame, text='Enter Your Password').grid(row=5, column=1, columnspan=3)
		Entry(frame, highlightbackground='Green', textvariable=password).grid(row=6, column=1, columnspan=3)
		Label(frame, text='Confirm Your Password').grid(row=7, column=1, columnspan=3)
		Entry(frame, highlightbackground='Green', textvariable=confirmPass).grid(row=8, column=1, columnspan=3)
		
		signUpButton = Button(frame, text='Sign Up', command=lambda:self.confirm(email, confirmEmail, password, confirmPass)).grid(row=9, column=1, columnspan=3)
		Button(frame, text='Return to Sign In Screen', command=lambda:self.backToSignIn()).grid(row=10, column=1, columnspan=3)
		
	def confirm(self, email, confirmEmail, password, confirmPassword):
		#Check that user's information matches and does not already exist in the database
			#If everything works out, go to main screen
			#Otherwise, stay here and display an error message
		def processData(authData):
			authData = authData.get()
			if len(authData) == 0 or 'code' not in authData or 'state' not in authData:
				Label(frame, text='Error').grid(row=3, column=1, columnspan=3)
				return
			else:
				global userData
				userData = api.decodeAuthData(authData)
				f.addAuthData(userData)
				mainMenu()
				
		email = email.get()
		password = password.get()
		confirmEmail = confirmEmail.get()
		confirmPassword = confirmPassword.get()
		if(self.checkInfo(email, confirmEmail, password, confirmPassword)):
			clearFrame(frame)
			if f.signUp(email, password):
				api.auth()
				authData = StringVar()
				clearFrame(frame)
				Label(frame, text='Copy address bar into text box below').grid(row=0, column=1, columnspan=3)
				Entry(frame, textvariable=authData).grid(row=1, column=1, columnspan=3)
				Button(frame, text='Confirm', command=lambda:processData(authData)).grid(row=2, column=1, columnspan=3)
			else:
				print('Error')
		else:
			print('No')
	def checkInfo(self, email, confirmEmail, password, confirmPassword):
		if email != confirmEmail or password != confirmPassword:
			return False
		else:
			return True
	def backToSignIn(self):
		clearFrame(frame)
		signIn()


class mainMenu():
	def __init__(self):
		clearFrame(frame)
		Label(frame, text='Main Menu').grid(row=0, column=1, columnspan=3)
		Button(frame, text='Clean A Playlist By Artist', command=lambda:playlistPick('cleanByArtists')).grid(row=1, column=1, columnspan=3)
		Button(frame, text='Clean A Playlist By Track', command=lambda:playlistPick('cleanByUser')).grid(row=2, column=1, columnspan=3)
		Button(frame, text='Reorder a Playlist', command=lambda:playlistPick('reorderPlaylist')).grid(row=3, column=1, columnspan=3)
		Button(frame, text='Revert a Playlist To Previous Version', command=lambda:playlistPick('revertPlaylist')).grid(row=4, column=1, columnspan=3)
		Button(frame, text='Add Tracks to a Playlist', command=lambda:playlistPick('addTracks')).grid(row=5, column=1, columnspan=3)
		Button(frame, text='Profile Manager', command=lambda:profileManager()).grid(row=6, column=1, columnspan=3)
		Button(frame, text='Get recommendations', command=lambda:recommendations()).grid(row=7, column=1, columnspan=3)
		Button(frame, text='Transfer from another music streaming service').grid(row=8, column=1, columnspan=3)
		Button(frame, text='Tranfer from a device').grid(row=9, column=1, columnspan=3)
		Button(frame, text='Sign Out', command=self.signOut).grid(row=10, column=1, columnspan=3)
		
	def signOut(self):
		def yes():
			api.signOutBrowser()
			no()
		def no():
			f.removeDevice()
			clearFrame(frame)
			signIn()
		clearFrame(frame)
		Label(frame, text='Would you also like to sign out of your browser?').grid(row=0, column=1, columnspan=3)
		Button(frame, text='Yes', command=yes).grid(row=1, column=1, columnspan=3)
		Button(frame, text='No', command=no).grid(row=2, column=1, columnspan=3)
class recommendations():
	def __init__(self):
		clearFrame(frame)
		data = api.getUserTopItems(userData)
		self.start(data)
		
	def start(self, data):
		recommendation = self.getRecommendation(data)
		recommendationData = StringVar()
		hold = 'Song Name: ' + recommendation['trackName'] + '\nGenre: ' + recommendation['genre'] + '\nArtist(s): '
		
		for i in recommendation['artistData']:
			hold = hold + ' ' + i['artistName'] + ' &'
		hold = hold[:-1]
		
		recommendationData.set(hold)
		Label(frame, textvariable=recommendationData).grid(row=0, column=1, columnspan=3)
		Button(frame, text='Add to Queue', command=lambda:self.addToQueue(recommendation, data)).grid(row=1, column=1, columnspan=3)
		Button(frame, text='Add to Playlist', command=None).grid(row=2, column=1, columnspan=3)
		Button(frame, text='Add to Track To Dislikes').grid(row=3, column=1, columnspan=3)
		Button(frame, text='Add Artist To Dislikes', command=self.addTrackToDislikes(recommendation)).grid(row=4, column=1, columnspan=3)
		Button(frame, text='Get New Recommendation', command=lambda:self.getNewRecommendation(data)).grid(row=5, column=1, columnspan=3)
		Button(frame, text='Return to Main Menu', command=mainMenu).grid(row=6, column=1, columnspan=3)
	
	def addTrackToDislikes(self, recommendation):
		f.addTrackDislikes(recommendation)
	def addArtistToDislikes(self, recommendation):
		f.addArtistToDislikes(recommendation)	
	def getNewRecommendation(self, data):
		clearFrame(frame)
		self.start(data)
		
	def getRecommendation(self, data):
		genres = data['topGenres']
		artists = data['topArtists']
		index = random.randint(0, len(genres))
		genre = genres[index]['genre']
		dat = f.getDislikedData()
		dislikedArtists = dat['dislikedArtists']
		dislikedTracks = dat['dislikedTracks']
		offset = random.randint(0, 100)
		hold = api.genreSearch(genre, userData, offset)
		if dislikedArtists == None and dislikedTracks == None:
			return hold
		elif dislikedArtists == None:
			while hold['trackId'] in dislikedTracks:
				offset = random.randint(0, 100)
				hold = api.genreSearch(genre, userData, offset)
		elif dislikedTracks == None:
			while hold['artistData'][0]['artistId'] in dislikedArtists:
				offset = random.randint(0, 100)
				hold = api.genreSearch(genre, userData, offset)
		else:
			while hold['artistData'][0]['artistId'] in dislikedArtists and hold['trackId'] in dislikedTracks:
				offset = random.randint(0, 100)
				hold = api.genreSearch(genre, userData, offset)
		return hold
	
	def addToQueue(self, trackInfo, data):
		message = api.addToQueue(trackInfo['trackUri'], userData)
		trackName = trackInfo['trackName']
		l = Label(frame)
		if message == 'Great Success':
			l.configure(text=f'{trackName} successfully added to queue')
			l.grid(row=10, column=1, columnspan=3)
		else:
			devices = api.getDeviceList(userData)
			if devices == None:
				print('Do Something')
			else:
				l.configure(text='Please select a device')
				lb = Listbox(frame, selectmode=SINGLE)
				for i in devices['deviceNames']:
					lb.insert(END, i)
				l.grid(row=7, column=1, columnspan=3)
				lb.grid(row=8, column=1, columnspan=3)
				Button(frame, text='Add Track to this Device\'s Queue', command=lambda:selectDevice(lb.curselection(), devices)).grid(row=9, column=1, columnspan=3)
		def selectDevice(selection, deviceList):
			deviceId = deviceList['deviceIds'][selection[0]]
			x = api.addToDeviceQueue(trackInfo['trackUri'], userData, deviceId)
			if x == 'Great Success':
				clearFrame(frame)
				self.getNewRecommendation(data)
			else:
				print('Do Something')
		
class profileManager():
	def __init__(self):
		clearFrame(frame)
		self.init()
	def init(self):
		Label(frame, text='Select the operations below').grid(row=0, column=1, columnspan=3)
		Button(frame, text='Unfollow Artists', command=self.unfollowArtists).grid(row=1, column=1, columnspan=3)
		Button(frame, text='Follow Artists').grid(row=2, column=1, columnspan=3)
		Button(frame, text='Back to Main Menu', command=mainMenu).grid(row=3, column=1, columnspan=3)
		
	def unfollowArtists(self):
		def unfollowSelection():
			selected = lb.curselection()
			ids = []
			for i in selected:
				ids.append(data[i]['id'])
			api.unfollowSelectedArtists(ids, userData)
		def selectAll():
			lb.select_set(0, END)
		clearFrame(frame)
		data = api.getFollowedArtists(userData)
		if(len(data) == 0):
			Label(frame, text='There are no artists to unfollow').grid(row=10, column=1, columnspan=3)
			self.init()
		else:
			Label(frame, text='Select Artists to Unfollow').grid(row=1, column=1, columnspan=3)
			lb = Listbox(frame, selectmode=MULTIPLE)
			for i in data:
				hold = i['name']
				lb.insert(END, hold)
			lb.grid(row=2, column=1, columnspan=3)
			Button(frame, text='Select All', command=selectAll).grid(row=3, column=1, columnspan=3)
			Button(frame, text='Confirm Selection(s)', command=lambda: unfollowSelection()).grid(row=4, column=1, columnspan=3)
			Button(frame, text='Back to Main Menu', command=mainMenu).grid(row=5, column=1, columnspan=3)
	
	def followArtists(self):
		clearFrame(frame)
	
class playlistPick():
	def __init__(self, nextScreen):
		clearFrame(frame)
		root.title('Pick a Playlist')
		playlists = api.getUserPlaylists(userData)
		Label(frame, text='Pick a Playlist').grid(row=0, column=1, columnspan=3)
		lb = Listbox(frame, selectmode=SINGLE)
		for i in playlists:
			hold = i['name']
			lb.insert(END, hold)
		lb.grid(row=1, column=1, columnspan=3)
		Button(frame, text='Confirm Playlist Selection', command=lambda:self.confirm(nextScreen, lb.curselection(), playlists)).grid(row=2, column=1, columnspan=3)
		Button(frame, text='Back to main menu', command=lambda:mainMenu()).grid(row=3, column=1, columnspan=3)
		f.addUserPlaylists(playlists)
	def confirm(self, nextScreen, selection, playlists):
		#Make sure an item has been selected
			#If selection is blank, stay on screen and display an error message
			#Otherwise continue to opScreen
		selection = playlists[selection[0]]
		clearFrame(frame)
		opScreen(nextScreen, selection)
		
		
		
class opScreen():
	def __init__(self, nextScreen, selection):
		self.ops(nextScreen, selection)
		
	def ops(self, nextScreen, selection):

		l = Label(frame)
		lb = Listbox(frame, selectmode=MULTIPLE, width=50)
		playlistName = selection['name']
		dat = {
			'playlistName': selection['name'],
			'playlistId': selection['id'],
			'snapshot_id': selection['snapshotId']
		}
		if(nextScreen == 'cleanByArtists'):
			l.configure(text=f'Please select one or more artists to delete from {playlistName}')
			dat['data'] = api.artistsAndTracks(selection['id'], userData)
			for i in dat['data']:
				artName = i['artistName']
				if artName == "":
					artName = '_________'
				artTrackCount = len(i['artistTrackNames'])
				hold = f'{artName}\t\t{artTrackCount}'
				lb.insert(END, hold)
			l.grid(row=0, column=1, columnspan=3)
		
			lb.grid(row=3, column=1, columnspan=3)
			Button(frame, text='Confirm Selection(s)', command=lambda:self.deleteTracks(nextScreen, lb.curselection(), dat)).grid(row=4, column=1, columnspan=3)
			Button(frame, text='Back to playlist selection', command=lambda:playlistPick(nextScreen)).grid(row=5, column=1, columnspan=3)
			Button(frame, text='Back to Main Menu', command=lambda:mainMenu()).grid(row=6, column=1, columnspan=3)
		elif(nextScreen == 'cleanByUser'):
			l.configure(text=f'Please select one or more tracks to delete from {playlistName}')
			dat['data'] = api.playlistTracks(selection['id'], userData)['data']
			for i in dat['data']:
				hold = i['trackName']
				hold = f"{hold:<80}"
				for j in i['artistNames']:
					hold = hold + ' ' + j + '/'
				hold = hold[:-1]
				lb.insert(END, hold)
			l.grid(row=0, column=1, columnspan=3)
		
			lb.grid(row=3, column=1, columnspan=3)
			Button(frame, text='Confirm Selection(s)', command=lambda:self.deleteTracks(nextScreen, lb.curselection(), dat)).grid(row=4, column=1, columnspan=3)
			Button(frame, text='Back to playlist selection', command=lambda:playlistPick(nextScreen)).grid(row=5, column=1, columnspan=3)
			Button(frame, text='Back to Main Menu', command=lambda:mainMenu()).grid(row=6, column=1, columnspan=3)	
		elif(nextScreen == 'reorderPlaylist'):
			l.configure(text=f'Reorder tracks within {playlistName}')
		elif(nextScreen == 'revertPlaylist'):
			l.configure(text=f'Select a previous version of {playlistName}')
			l.grid(row=0, column=1, columnspan=3)
			dat = f.getPlaylistVersions(selection['id'])
			for i in range(0, len(dat)):
				trackCount = dat[i]['trackCount']
				hold = f'Version number {i} \t {trackCount}'
				lb.insert(END, hold)
			lb.grid(row=3, column=1, columnspan=3)
			Button(frame, text='Confirm Selection(s)', command=lambda:self.revertPlaylist(dat, lb.curselection(), selection['id'])).grid(row=4, column=1, columnspan=3)
			Button(frame, text='Back to playlist selection', command=lambda:playlistPick(nextScreen)).grid(row=5, column=1, columnspan=3)
			Button(frame, text='Back to Main Menu', command=lambda:mainMenu()).grid(row=6, column=1, columnspan=3)
		elif nextScreen == 'addTracks':
			l.configure(text=f'Search for an artist or track to add to {playlistName}')
			search = StringVar()
			l.grid(row=0, column=1, columnspan=3)
			Entry(frame, textvariable=search).grid(row=1, column=1, columnspan=3)
			Button(frame, text='Confirm', command=lambda:self.search(search, selection)).grid(row=1, column=4, columnspan=3)
			Button(frame, text='Back to main menu', command=lambda:mainMenu()).grid(row=5, column=1, columnspan=1)
					
	def revertPlaylist(self, data, selected, playlistId):
		trackRefs = data[selected[0]]['trackRefs']
		
		playlist = api.playlistTracks(playlistId, userData)
		playlistIds = playlist['ids']
		#If in playlistIds but not in trackRefs, delete from spotify playlist
		#If in trackRefs but not in trackRefs, add to spotify playlist
		#If in both, do nothing
		deleteIds = []
		addIds = []
		keepIds = []
		addUris = []
		i = 0
		j = 0
		
		while i < len(trackRefs) and j < len(playlistIds):
			if trackRefs[i] not in playlistIds and trackRefs[i] not in addIds:
				addIds.append(trackRefs[i])
			else:
				keepIds.append(trackRefs[i])
			i = i + 1
			if playlistIds[j] not in trackRefs and playlistIds[j] not in deleteIds:
				deleteIds.append(playlistIds[j])
			else:
				keepIds.append(playlistIds[j])
			j = j + 1
		if len(deleteIds) > 0:
			api.deleteTracks(deleteIds, playlistIds, userData)
		if len(addIds) > 0:
			api.addTracks(playlistId, addIds, userData)
		mainMenu()
		
	
	def search(self, searchFor, selection):
		data = api.search(searchFor, userData)
		lb = Listbox(frame, selectmode=MULTIPLE, width=100)
		for i in data:
			hold = i['trackName'] + ' | \t' + i['albumName'] + '| \t'
			if i['explicit']:
				hold = hold + 'Explicit' + ' | \t'
			else:
				hold = hold + 'Not Explicit' + ' | \t'
				
			for j in i['artists']:
				hold = hold +  '\t' + j + ', '
			hold = hold[:-1]
			lb.insert(END, hold)
		lb.grid(row=3, column=1, columnspan=4)
		Button(frame, text='Confirm Selection(s)', command=lambda:self.confirmSelections(lb.curselection(), selection, data)).grid(row=4, column=1, columnspan=3)
	def confirmSelections(self, selections, playlistSelection, data):
		trackIds = []
		for i in selections:
			trackIds.append(data[i]['trackId'])
		api.addTracks(playlistSelection['id'], trackIds, userData)
		self.ops('addTracks', playlistSelection)
	def deleteTracks(self, nextScreen, selected, data):
		
		trackIds = []
		trackUris = []
		playlistData = data['data']
		if nextScreen == 'cleanByArtists':
			for i in selected:
				trackIds.extend(playlistData[i]['artistTrackIds'])
				trackUris.extend(playlistData[i]['artistTrackUris'])
		elif nextScreen == 'cleanByUser':
			for i in selected:
				trackIds.append(playlistData[i]['trackId'])
				trackUris.append(playlistData[i]['trackUri'])
		
		clearFrame(frame)
		Label(frame, text='Would you like to save the previous version of your playlist?').grid(row=0, column=1, columnspan=3)
		Button(frame, text='Yes', command=lambda:self.chooseToSave(True, {'trackUris': trackUris, 'trackIds': trackIds}, userData, data, nextScreen)).grid(row=1, column=1, columnspan=3)
		Button(frame, text='No', command=lambda:self.chooseToSave(False, {'trackUris': trackUris, 'trackIds': trackIds}, userData, data, nextScreen)).grid(row=2, column=1, columnspan=3)
		Button(frame, text='Back to main', command=lambda:mainMenu()).grid(row=3, column=1, columnspan=3)
	
	def chooseToSave(self, save, trackData, userData, playlistData, nextScreen):
		if save:
			f.saveVersion(playlistData, nextScreen)
		#Delete Tracks
		api.deleteTracks(trackData, playlistData, userData)
		clearFrame(frame)
		mainMenu()

def clearFrame(frame):
	for i in frame.winfo_children():
		i.destroy()

def rememberDevice(var):
	var = var.get()
	if var == 1:
		mac = get_mac()
	else:
		mac = None
	return mac	

f = fire()
root = Tk()
root.attributes('-fullscreen',True)
root.state('zoomed')
frame = Frame(root)
frame.pack()
api = apiInteraction()
a = signIn()
root.mainloop()
