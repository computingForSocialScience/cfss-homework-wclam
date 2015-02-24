import sys
import random
from io import open
from artistNetworks import *
from analyzeNetworks import *
from fetchArtist import *
from fetchAlbums import *

def fetchTrackNames(album_id):
	url = 'https://api.spotify.com/v1/albums/' + album_id + '/tracks'
   	req = requests.get(url)
   	data = req.json()
   	track_list = []
   	for track in data['items']:
   		track_list.append(track['name'])
   	return track_list

if __name__ == '__main__':
	artist_names = sys.argv[1:]
	print 'input artists are', artist_names

#fetch artistNetworks
	artist_ids = []
	for name in artist_names:
		id = fetchArtistId(name)
		artist_ids.append(id)

#make edgelist for first artist input
	edgeList = getEdgeList(artist_ids[0], depth=2)

#create list of artist networks
	for i in range(len(artist_ids)):
		if i == 0:
			continue
		else:
			edgeList = combineEdgeLists(edgeList, getEdgeList(artist_ids[i], 2))
#convert to networkx
	def pandasToNetworkX2(edgeList):
		graph = nx.DiGraph()
		df = pd.DataFrame(edgeList)
		if len(df.columns) > 2:
			print "Warning: more than two columns. Returning only first two"
			df = df[df.columns[0:2]]
		edges = df.to_records(index=False)
		graph.add_edges_from(edges)
		#print graph.edges()
		return graph

#convert to networkx
	g = pandasToNetworkX2(edgeList)
#collect random sample
	k = 0
	playlist = []
	while k != 30:
		artist_dict = {}
		artist_dict['artist_name'] = fetchArtistInfo(randomCentralNode(g))['name']
		album_id = np.random.choice(fetchAlbumIds(fetchArtistId(artist_dict['artist_name'])))
		artist_dict['album_name'] = fetchAlbumInfo(album_id)['name']
		artist_dict['track_name'] = np.random.choice(fetchTrackNames(album_id))
		playlist.append(artist_dict)
		k += 1

#playlist
	f = open("playlist.csv", "w", encoding = 'utf-8')
	try:
		f.write('"%s", "%s", "%s"\n' % (u'artist_name',u'album_name',u'track_name'))
		for i in playlist:
			artist_name = i['artist_name']
			album_name = i['album_name']
			track_name = i['track_name']
			f.write('"%s", "%s", "%s"\n' % (artist_name, album_name, track_name))
	finally:
		f.close()