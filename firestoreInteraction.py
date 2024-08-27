import firebase_admin
import base64
from firebase_admin import credentials
from firebase_admin import firestore

class fire():
	def __init__(self):
		global db
		global app
		if not firebase_admin._apps:
			cred = credentials.Certificate('/Users/danielwarren/Desktop/Spotify App Version 3/cred/spotifyproject2-b207f-firebase-adminsdk-uhi0q-54ac540e60.json')
			app = firebase_admin.initialize_app(cred)
		db = firestore.client()
	
	def signUp(self, email, password):
		data_bytes = email.encode("utf-8")
		global id
		id = base64.b64encode(data_bytes)
		ref = db.collection('Users').document(str(id))
		doc = ref.get()
		
		passBytes = password.encode("utf-8")
		encodedPass = base64.b64encode(passBytes)
		
		if doc.exists:
			print('User already exists')
			return False
		else:
			ref.set({
				'Email': id,
				'Password': encodedPass,
				'Playlists': [],
				'Settings': []
			})
			return True
	def addAuthData(self, data):
		ref = db.collection('Users').document(str(id))
		ref.update({
			'authData': data			
		})
	def retrieveAuthData(self, email, password):
		data_bytes = email.encode("utf-8")
		global id
		id = base64.b64encode(data_bytes)
		
		doc = db.collection('Users').document(str(id)).get()
		if doc.exists:
			hold = doc.to_dict()
			passFire = hold['Password']
			passFire = base64.b64decode(passFire)
			passFire = passFire.decode('utf-8')
			if passFire == password:
				return hold['authData']
			else:
				return 'Invalid Email/Password'
		else:
			return 'Invalid Email/Password'
		
	def addUserPlaylists(self, playlists):
		ref = db.collection('Playlists')
		for i in playlists:
			holdId = i['id'] + str(id)
			ref = db.collection('Playlists').document(holdId).get()
			if not ref.exists:
				ref = db.collection('Playlists').document(holdId).set({
					'ownerId': str(id),
					'VersionCount': 0,
				})
	def saveVersion(self, playlistData, nextScreen):
		if nextScreen == 'cleanByArtists':
			data = []
			trackIds = []
			for i in playlistData['data']:
				for j in range(0, len(i['artistTrackIds'])):
					if i['artistTrackIds'][j] in trackIds:
						data[trackIds.index(i['artistTrackIds'][j])]['artistNames'].append(i['artistName'])
					else:
						trackIds.append(i['artistTrackIds'][j])
						data.append({
							'trackName': i['artistTrackNames'][j],
							'trackId': i['artistTrackIds'][j],
							'artistNames': [i['artistName']]
						})
		else:
			data = playlistData['data']
		playlistId = playlistData['playlistId'] + str(id)
		playlistRef = db.collection('Playlists').document(playlistId)
		playlistDoc = playlistRef.get().to_dict()
		versionId = playlistId + str(playlistDoc['VersionCount'])
		versionRef = db.collection('Playlists').document(playlistId).collection('Versions').document(versionId)
		trackRefs = []
		for i in data:
			trackRef = db.collection('Tracks').document(i['trackId'])
			check = trackRef.get()
			if not check.exists:
				trackRef.set({
					'artistNames': i['artistNames'],
					'trackName': i['trackName']
				})
			trackRefs.append(i['trackId'])
		versionRef.set({
			'trackCount': len(trackRefs),
			'trackRefs': trackRefs
		})
		versionCount = playlistDoc['VersionCount'] + 1
		
		playlistRef.update({
			'VersionCount': versionCount
		})
	
	def rememberDevice(self, mac):
		ref = db.collection('Users').document(str(id))
		dev = base64.b64encode(str(mac).encode("utf-8"))
		ref.update({
			'Device': dev
		})
				
	def checkForDevice(self, mac):			
		dev = base64.b64encode(str(mac).encode("utf-8"))
		ref = db.collection('Users').where('Device', '==', dev).get()
		if len(ref) == 0:
			return None
		doc = ref[0].to_dict()
		global id
		id = ref[0].id
		return doc
	
	def removeDevice(self):
		ref = db.collection('Users').document(str(id))
		ref.update({
			'Device': None
		})
		
	def getPlaylistVersions(self, selection):
		versionData = []
		playlistId = selection + str(id)
		i = 0
		ref = db.collection('Playlists').document(playlistId).collection('Versions').document(f'{playlistId}{i}').get()
		while ref.exists:
			hold = ref.to_dict()
			hold['versionId'] = ref.id
			versionData.append(hold)
			i = i + 1
			ref = db.collection('Playlists').document(playlistId).collection('Versions').document(f'{playlistId}{i}').get()
		return versionData
	
	def addTrackDislikes(self, trackData):
		trackId = trackData['trackId']
		ref = db.collection('Users').document(str(id)).update({'dislikedTracks': firestore.ArrayUnion([trackId])})
	
	def addArtistToDislikes(self, trackData):
		artistId = trackData['artistData'][0]['artistId']
		ref = db.collection('Users').document(str(id)).update({'dislikedArtists': firestore.ArrayUnion([artistId])})
	
	def getDislikedData(self):
		ref = db.collection('Users').document(str(id)).get()
		doc = ref.to_dict()
		
		if 'dislikedArtists' in doc and 'dislikedTracks' in doc:
			dislikedArtists = doc['dislikedArtists']
			dislikedTracks = doc['dislikedTracks']
			return {
				'dislikedArtists': dislikedArtists,
				'dislikedTracks': dislikedTracks
			}
		elif 'dislikedTracks' in doc:
			dislikedTracks = doc['dislikedTracks']
			return {
				'dislikedTracks': dislikedTracks,
				'dislikedArtists': None
			}
		elif 'dislikedArtists' in doc:
			dislikedArtists = doc['dislikedArtists']
			return {
				'dislikedArtists': dislikedArtists,
				'dislikedTracks': None
			}
		else:
			return{
				'dislikedArtists': None,
				'dislikedTracks': None	
			}
		