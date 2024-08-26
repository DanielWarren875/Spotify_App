import json
import random
import string
from typing import Counter
import webbrowser
import requests
import base64

from firestoreInteraction import fire

class apiInteraction():
	def auth(self):
			global c
			global redirect
			c = 'bf9fd0131e0a4c56ab5ec69dc87befc3'
			redirect = 'http://localhost:80'
			chars = string.ascii_lowercase + string.digits
			state = ''.join(random.choice(chars) for i in range(16))
			scope = 'user-read-private,user-read-email,playlist-read-private,user-library-read,playlist-read-collaborative,user-library-modify,playlist-modify-private,playlist-modify-public,user-follow-read,playlist-modify-public,playlist-modify-private,user-top-read,user-read-private,user-read-email,user-follow-modify,user-modify-playback-state'
			type = 'code'
			url = f'http://accounts.spotify.com/authorize?response_type={type}'
			url = url + f'&client_id={c}&scope={scope}'
			url = url + f'&redirect_uri={redirect}&state={state}'
			webbrowser.open(url)
	def decodeAuthData(self, authData):
		grantType = 'authorization_code'
		code = authData[authData.find('code=') + 5: authData.find('&state')]
		s = '9ab7c1a94f2841d6bb97102680edd97d'
		data = {
			'grant_type': grantType,
			'code': code,
			'redirect_uri': redirect
		}
		encode = base64.urlsafe_b64encode((c + ':' + s).encode())
		header = {
			'Authorization': 'Basic %s' %encode.decode('ascii'),
			'Content-Type': 'application/x-www-form-urlencoded'
		}
		url = 'https://accounts.spotify.com/api/token'
		r = requests.post(url=url, headers=header, data=data)
		
		x = json.loads(r.text)
		return {
			'access_token': x['access_token'],
			'token_type': x['token_type'],
			'expires_in': x['expires_in'],
			'refresh_token': x['refresh_token'],
			'scope': x['scope']
		}
	
	def refreshToken(self, authData):
		c = 'bf9fd0131e0a4c56ab5ec69dc87befc3'
		s = '9ab7c1a94f2841d6bb97102680edd97d'
		data = {
			'grant_type': 'refresh_token',
			'refresh_token': authData['refresh_token'],
		}
		encode = base64.urlsafe_b64encode((c + ':' + s).encode())
		headers = {
			'Content-Type': 'application/x-www-form-urlencoded',
			'Authorization': 'Basic %s' %encode.decode('ascii')
		}
		url = 'https://accounts.spotify.com/api/token'
		r = requests.post(url=url, headers=headers, data=data)
		x = json.loads(r.text)
		return x
	
	def getUserPlaylists(self, data):
		url = 'https://api.spotify.com/v1/me/playlists'
		header = {
			'Authorization': data['token_type'] + ' ' + data['access_token']
		}
		r = requests.get(url=url, headers=header)
		x = json.loads(r.text)
		items = x['items']
		
		y = self.getUserProfile(data)
		user = y['display_name']
		playlistInfo = [{
			'id': 'me',
			'name': 'Liked Playlist',
			'snapshotId': 'None'
		}]
		
		for i in items:
			owner = i['owner']['id']
			if user != owner and i['collaborative'] == False:
				continue
			else:
				id = i['id']
				name = i['name']
				snapshot = i['snapshot_id']
				hold = {
					'id': id,
					'name': name,
					'snapshotId': snapshot
				}
				playlistInfo.append(hold)
		return playlistInfo
	
	
				
		
	def getUserProfile(self, data):
		url = 'https://api.spotify.com/v1/me'
		header = {
			'Authorization': data['token_type'] + ' ' + data['access_token']
		}
		r = requests.get(url=url, headers=header)
		
		x = json.loads(r.text)
		return x
	
	
	def artistsAndTracks(self, playlistId, authData):
		if playlistId == 'me':
			url = f'https://api.spotify.com/v1/me/tracks?limit=50'
		else:	
			url = f'https://api.spotify.com/v1/playlists/{playlistId}/tracks?limit=50'
		header = {
			'Authorization': authData['token_type'] + ' ' + authData['access_token']
		}
		
		data = []
		artists = []
		while url != None:
			r = requests.get(url=url, headers=header)
			x = json.loads(r.text)
			next = x['next']
			items = x['items']
			for i in items:
				track = i['track']
				arts = track['artists']
				for j in arts:
					if j['name'] not in artists:
						data.append({
							'artistName': j['name'],
							'artistId': j['id'],
							'artistTrackNames': [track['name']],
							'artistTrackIds': [track['id']],
							'artistTrackUris': [track['uri']]
						})
						artists.append(j['name'])
					else:
						loc = artists.index(j['name'])
						data[loc]['artistTrackNames'].append(track['name'])
						data[loc]['artistTrackIds'].append(track['id'])
			url = next
		data = sorted(data, key=lambda x:x['artistName'])
		return data	
		
	def playlistTracks(self, playlistId, authData):
		if playlistId == 'me':
			url = f'https://api.spotify.com/v1/me/tracks?limit=50'
		else:	
			url = f'https://api.spotify.com/v1/playlists/{playlistId}/tracks?limit=50'
		header = {
			'Authorization': authData['token_type'] + ' ' + authData['access_token']
		}
		
		data = []
		ids = []
		uris = []
		while url != None:
			r = requests.get(url=url, headers=header)
			x = json.loads(r.text)
			next = x['next']
			items = x['items']
			
			for i in items:
				track = i['track']
				hold = {
					'trackName': track['name'],
					'trackId': track['id'],
					'trackUri': track['uri'],
					'artistNames': []
				}
				ids.append(track['id'])
				uris.append(track['uri'])
				artists = track['artists']
				for j in artists:
					hold['artistNames'].append(j['name'])
				data.append(hold)
			url = next
		return {
			'data': data,
			'ids': ids,
			'uris': uris
		}
	
	def deleteTracks(self, trackData, playlistData, authData):
		tracksToBeDeleted = []
		header = {
				'Authorization': authData['token_type'] + ' ' + authData['access_token'],
				'Content-Type': 'application/json'
		}
		playlistId = playlistData['playlistId']
		if playlistId == 'me':
			url = 'https://api.spotify.com/v1/me/tracks?ids='
			trackIds = trackData['trackIds']
			for i in trackIds:
				url = url + i + ','
				tracksToBeDeleted.append(i)
				if len(tracksToBeDeleted) == 20:
					url = url[:-1]
					x = json.dumps({'data': {
						'ids': tracksToBeDeleted
					}})
					r = requests.delete(url=url, headers=header, data=x)
					url = 'https://api.spotify.com/v1/me/tracks?ids='
					tracksToBeDeleted = []
			url = url[:-1]
			x = json.dumps({'data': {
				'ids': tracksToBeDeleted
			}})
			r = requests.delete(url=url, headers=header, data=x)
		else:
			print(trackData)
			
	def genreSearch(self, searchFor, authData, offset):
		searchFor.replace(' ', '+')
		header = {
			'Authorization': authData['token_type'] + ' ' + authData['access_token']
		}
		url = f'https://api.spotify.com/v1/search?q={searchFor}&type=track&offset={offset}&limit=1'
		r = requests.get(url=url, headers=header)
		
		x = json.loads(r.text)
		item = x['tracks']['items'][0]
		id = item['id']
		uri = item['uri']
		name = item['name']
		artistData = []
		for i in item['artists']:
			artistId = i['id']
			artistName = i['name']
			artistData.append({
				'artistId': artistId,
				'artistName': artistName
			})
		return {
			'trackId': id,
			'trackUri': uri,
			'trackName': name,
			'artistData': artistData,
			'genre': searchFor
		}
		
		
		
		
	def search(self, searchFor, authData):	
			searchFor = searchFor.get()
			searchFor.replace(' ', '+')
			url = f'https://api.spotify.com/v1/search?q={searchFor}&type=track&limit=50'
			header = {
				'Authorization': authData['token_type'] + ' ' + authData['access_token']
			}
			
			trackIds = []
			data = []
			
			while url != None:
				r = requests.get(url=url, headers=header)
				x = json.loads(r.text)
				next = x['tracks']['next']
				items = x['tracks']['items']
				for i in items:
					if i['id'] not in trackIds:
						hold = {
							'trackName': i['name'],
							'trackId': i['id'],
							'albumName': i['album']['name'],
							'explicit': i['explicit']
						}
						trackIds.append(i['id'])
						arts = i['artists']
						artistNames = []
						for j in arts:
							artistNames.append(j['name'])
						hold['artists'] = artistNames
						data.append(hold)
				url = next
			return data
	
	def addTracks(self, playlistId, trackIds, authData):			
		if playlistId == 'me':
			url = 'https://api.spotify.com/v1/me/tracks?ids='
			header = {
				'Authorization': authData['token_type'] + ' ' + authData['access_token'],
				'Content-Type': 'application/json'
			}
			first = 0
			for i in range(0, len(trackIds)):
				url = url + trackIds[i] + ','
				if i % 20 == 0 and i != 0:
					data = json.dumps({
						'ids': trackIds[first:i]
					})
					url = url[:-1]
					r = requests.put(url=url, headers=header, data=data)
					url = 'https://api.spotify.com/v1/me/tracks?ids='
					first = i + 1
			data = json.dumps({
				'ids': trackIds[first:len(trackIds)]
			})
			url = url[:-1]
			r = requests.put(url=url, headers=header, data=data)
		else:
			print('Wait')
			
	def getFollowedArtists(self, authData):
		url = f'https://api.spotify.com/v1/me/following?type=artist'
		header = {
			'Authorization': authData['token_type'] + ' ' + authData['access_token']
		}
		data = []
		while url != None:
			r = requests.get(url=url, headers=header)
			x = json.loads(r.text)
			artists = x['artists']
			next = artists['next']
			
			for i in artists['items']:
				name = i['name']
				id = i['id']
				data.append({
					'name': name,
					'id': id
				})
			url = next
		return data
	def unfollowSelectedArtists(self, ids, authData):
		header = {
			'Authorization': authData['token_type'] + ' ' + authData['access_token'],
			'Content-Type': 'application/json'
		}
		url = 'https://api.spotify.com/v1/me/following?type=artist&ids='
		data = []
		for i in ids:
			url = url + i + ','
			data.append(i)
			if(len(data) == 20):
				url = url[:-1]
				x = json.dumps({'ids': data})
				r = requests.delete(url=url, headers=header, data=x)
				url = 'https://api.spotify.com/v1/me/following?type=artist&ids='
				data = []
		url = url[:-1]
		x = json.dumps({'ids': data})
		r = requests.delete(url=url, headers=header, data=x)
		data = []
	def signOutBrowser(self):
		url = 'https://www.spotify.com/logout'
		webbrowser.open(url)
	
	
	def getUserTopItems(self, authData):
		def getArtistGenres(artistId):
			url1 = f'https://api.spotify.com/v1/artists/{artistId}'
			r = requests.get(url=url1, headers=header)
			x = json.loads(r.text)
			genre = x['genres']
			for i in genre:
				if i not in genres:
					genres.append({
						'genre': i,
						'count': 1
					})
				else:
					genres[genres.index(j)]['count'] += 1 
		url = 'https://api.spotify.com/v1/me/top/artists?time_range=medium_term'
		header = {
			'Authorization': authData['token_type'] + ' ' + authData['access_token']
		}
		genres = []
		artists = []
		
		while url != None:
			r = requests.get(url=url, headers=header)
			x = json.loads(r.text)
			url = x['next']
			items = x['items']
			
			for i in items:
				genre = i['genres']
				artist = i['name']
				if artist not in artists:
					artists.append(artist)
				for j in genre:
					if j not in genres:
						genres.append({
							'genre': j,
							'count': 1
						})
					else:
						genres[genres.index(j)]['count'] += 1 
		
		url = 'https://api.spotify.com/v1/me/top/tracks?time_range=short_term'
		while url != None and len(artists) < 250 and len(genres) < 350:
			r = requests.get(url=url, headers=header)
			x = json.loads(r.text)
			url = x['next']
			items = x['items']
			for i in items:
				artist = i['artists']
				for j in artist:
					artName = j['name']
					if artName not in artists:
						artistId = j['id']
						getArtistGenres(artistId)
						artists.append(j['name'])
		return {
			'topArtists': artists,
			'topGenres': genres
		}
	def addToQueue(self, trackUri, authData):
		url = f'https://api.spotify.com/v1/me/player/queue?uri={trackUri}'
		header = {
			'Authorization': authData['token_type'] + ' ' + authData['access_token']
		}
		
		r = requests.post(url=url, headers=header)
		if "error" in r.text:
			x = json.loads(r.text)
			message = x['error']['message']
		else:
			message = 'Great Success'
		return message
	def addToDeviceQueue(self, trackUri, authData, deviceId):
		url = f'https://api.spotify.com/v1/me/player/queue?uri={trackUri}&device_id={deviceId}'
		header = {
			'Authorization': authData['token_type'] + ' ' + authData['access_token']
		}
		
		r = requests.post(url=url, headers=header)
		if "error" in r.text:
			x = json.loads(r.text)
			message = x['error']['message']
		else:
			message = 'Great Success'
		return message
	def getDeviceList(self, authData):
		url = f'https://api.spotify.com/v1/me/player/devices'
		header = {
			'Authorization': authData['token_type'] + ' ' + authData['access_token']
		}
		
		r = requests.get(url=url, headers=header)
		x = json.loads(r.text)
		deviceList = x['devices']
		
		if len(deviceList) == 0:
			return None
		else:
			deviceNames = []
			deviceIds = []
			
			for i in deviceList:
				hold = i['name']
				deviceNames.append(hold)
				hold = i['id']
				deviceIds.append(hold)
			return {
				'deviceNames': deviceNames,
				'deviceIds': deviceIds
			}
		
#userData = {'access_token': 'BQAAdTPg48eFYsV1KqiZgX0QJrsOnMfp713cJooQBkUJvud4d0YKJ5oezc8Gns7YBh1GDOrIpHk-DY-aykzDuM9w1FEg9Gh6kHTxdD43bsUVRG1955EJUs55k8PqbKoCx9usLDKYUNFfVPC950hHc0u_VGxacqnJRvNyMunfFG7Oxmf-aa79m-KNhgEGeSu9B72-bLIfSXqGSeku-DhLakfssvqld4xacyv3Wll_utgf1Uh7mfRnNabDMYdTGkdhN7qcXnAtqnL29XgbPEu4fTbQTPwYisJAfRSSXN_d6g1bEw', 'token_type': 'Bearer', 'expires_in': 3600, 'scope': 'playlist-read-private playlist-read-collaborative user-modify-playback-state ugc-image-upload user-library-read user-library-modify playlist-modify-private playlist-modify-public user-read-playback-state user-read-email user-read-recently-played user-read-private'}
#api = apiInteraction()
#f = fire()
#userData = f.retrieveAuthData('hold', 'hold')
#api.search('Vendetta Fit for a king', userData)