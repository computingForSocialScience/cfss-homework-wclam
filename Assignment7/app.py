from flask import Flask, render_template, request, redirect, url_for
import pymysql
from artistNetworks import *
from analyzeNetworks import *
from fetchArtist import *
from fetchAlbums import *
from makePlaylist import *

dbname="playlists"
host="localhost"
user="root"
passwd="Forest14"
db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')

app = Flask(__name__)

def fetchTrackNames(album_id):
    url = 'https://api.spotify.com/v1/albums/' + album_id + '/tracks'
    req = requests.get(url)
    data = req.json()
    track_list = []
    for track in data['items']:
        track_list.append(track['name'])
    return track_list

def createNewPlaylist(artist):
    artistID = fetchArtistId(artist)

#make edgelist for first artist input
    edgeList = getEdgeList(artistID, depth=2)

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
    
    cur = db.cursor()

    CreatePlaylist = '''CREATE TABLE IF NOT EXISTS playlists (id INTEGER PRIMARY KEY AUTO_INCREMENT, rootArtist VARCHAR(100));'''
    CreateSongs = '''CREATE TABLE IF NOT EXISTS songs (playlistId INTEGER, songOrder INTEGER, artistName VARCHAR(255), albumName VARCHAR(255), trackName VARCHAR(255));'''

    cur.execute(CreatePlaylist)
    cur.execute(CreateSongs)

    insertRootArtist = '''INSERT INTO playlists (rootArtist) VALUES (%s);'''
    cur.execute(insertRootArtist, artist)

    playlistId = cur.lastrowid
    k = 0
    playlist = []
    while k != 30:
        artist_name = fetchArtistInfo(randomCentralNode(g))['name']
        album_id = np.random.choice(fetchAlbumIds(fetchArtistId(artist_name)))
        album_name = fetchAlbumInfo(album_id)['name']
        track_name = np.random.choice(fetchTrackNames(album_id))
        playlist.append((playlistId, k, artist_name, album_name, track_name))
        k += 1

    insertQuery = '''insert into songs (playlistId, songOrder, artistName, albumName, trackName)
    values (%s, %s, %s, %s, %s);'''

    cur.executemany(insertQuery,playlist)

    db.commit()
    cur.close()

 
@app.route('/')
def make_index_resp():
    # this function just renders templates/index.html when
    # someone goes to http://127.0.0.1:5000/
    return(render_template('index.html'))


@app.route('/playlists/')
def make_playlists_resp():
    cur = db.cursor()
    cur.execute('''select * from playlists''')
    playlists = cur.fetchall()
    cur.close()
    return render_template('playlists.html', playlists=playlists)


@app.route('/playlist/<playlistId>')
def make_playlist_resp(playlistId):
    cur = db.cursor()
    cur.execute('''select * from songs where playlistId = %s order by songOrder''' %playlistId)
    songs = cur.fetchall()
    print songs
    cur.close()
    return render_template('playlist.html',songs=songs)


@app.route('/addPlaylist/',methods=['GET','POST'])
def add_playlist():
    if request.method == 'GET':
        # This code executes when someone visits the page.
        return(render_template('addPlaylist.html'))
    elif request.method == 'POST':
        # this code executes when someone fills out the form
        artistName = request.form['artistName']
        # YOUR CODE HERE
        createNewPlaylist(artistName)
        return(redirect("/playlists/"))



if __name__ == '__main__':
    app.debug=True
    app.run()

#createNewPlaylist("Nirvana")