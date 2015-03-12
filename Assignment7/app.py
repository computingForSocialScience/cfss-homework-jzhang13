from flask import Flask, render_template, request, redirect, url_for
import pymysql
from makePlaylist import *
from artistNetworks import *
from analyzeNetworks import *

dbname="playlists"
host="localhost"
user="root"
passwd="Scarlet423"
db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')

app = Flask(__name__)

def createNewPlaylist(artist_name):
    cur = db.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS playlists (id INTEGER PRIMARY KEY AUTO_INCREMENT,rootArtist VARCHAR(255));''')
    cur.execute('''CREATE TABLE IF NOT EXISTS songs (playlistId INTEGER,songOrder INTEGER,artistName VARCHAR(255),albumName VARCHAR(255),trackName VARCHAR(255));''')
    cur.execute('INSERT INTO playlists (rootArtist) VALUES (%s);', artist_name)
    p_id = cur.lastrowid
    edges = getEdgeList(fetchArtistId(artist_name), 2)
    dg = pandasToNetworkX(edges)
    artists = []
    for i in range(30):
        artists.append(randomCentralNode(dg))
    songs = []
    for a in artists:
        name = fetchArtistInfo(a)['name']
        try:
            album_id = random.choice(fetchAlbumIds(a))
        except:
            print 'artist %s has no albums' % name
            continue
        album_name = fetchAlbumInfo(album_id)['name']
        url = "https://api.spotify.com/v1/albums/" + album_id + "/tracks"
        req = requests.get(url)
        data = req.json()
        track_name = random.choice(data['items'])['name']
        songs.append((p_id, i, name, album_name, track_name))
        i = i + 1
    cur.executemany('''INSERT INTO songs (playlistId, songOrder, artistName, albumName, trackName) VALUES (%s, %s, %s, %s, %s);''', songs)
    db.commit()

    

@app.route('/')
def make_index_resp():
    # this function just renders templates/index.html when
    # someone goes to http://127.0.0.1:5000/
    return(render_template('index.html'))


@app.route('/playlists/')
def make_playlists_resp():
    cur = db.cursor()
    cur.execute('SELECT * FROM playlists;')
    playlists = cur.fetchall()
    return render_template('playlists.html',playlists=playlists)


@app.route('/playlist/<playlistId>')
def make_playlist_resp(playlistId):
    cur = db.cursor()
    cur.execute('SELECT songOrder, artistName, albumName, trackName FROM songs WHERE playlistId = %s ORDER BY songOrder;', playlistId)
    songs = cur.fetchall()
    return render_template('playlist.html',songs=songs)


@app.route('/addPlaylist/',methods=['GET','POST'])
def add_playlist():
    if request.method == 'GET':
        # This code executes when someone visits the page.
        return(render_template('addPlaylist.html'))
    elif request.method == 'POST':
        # this code executes when someone fills out the form
        artistName = request.form['artistName']
        createNewPlaylist(artistName)
        # YOUR CODE HERE
        return(redirect("/playlists/"))



if __name__ == '__main__':
    cur = db.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS playlists (id INTEGER PRIMARY KEY AUTO_INCREMENT,rootArtist VARCHAR(255));''')
    cur.execute('''CREATE TABLE IF NOT EXISTS songs (playlistId INTEGER,songOrder INTEGER, artistName VARCHAR(255), albumName VARCHAR(255), trackName VARCHAR(255));''')
    app.debug=True
    app.run()
