from flask import Flask, render_template, request, redirect, url_for
import pymysql
from downloadscript import *

app = Flask(__name__)

dbname="playlists"
host="localhost"
user="root"
passwd="Forest14"
db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')

@app.route('/')
def make_index_resp():
    # this function just renders templates/index.html when
    # someone goes to http://127.0.0.1:5000/
    return(render_template('index.html'))

#OLD PLS FIX BC BAD
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