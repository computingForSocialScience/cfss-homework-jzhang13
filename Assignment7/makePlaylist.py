import sys
import requests
import csv
import pandas as pd
import networkx as nx
import numpy
import random
from io import open
from artistNetworks import *
from analyzeNetworks import *
#from fetchArtist import fetchArtistId, fetchArtistInfo
#from fetchAlbums import fetchAlbumIds, fetchAlbumInfo

def fetchArtistId(name):
    """Using the Spotify API search method, take a string that is the artist's name, 
    and return a Spotify artist ID.
    """
    url = "https://api.spotify.com/v1/search?q=" + name + "&type=artist"
    req = requests.get(url)
    data = req.json()
    artistid = data['artists']['items'][0]['id']
    return artistid
    #pass

def fetchArtistInfo(artist_id):
    """Using the Spotify API, takes a string representing the id and
`   returns a dictionary including the keys 'followers', 'genres', 
    'id', 'name', and 'popularity'.
    """
    aDict = {}
    url = "https://api.spotify.com/v1/artists/" + artist_id
    req = requests.get(url)
    data = req.json()
    aDict['followers'] = data['followers']['total']
    aDict['genres'] = data['genres']
    aDict['id'] = data['id']
    aDict['name'] = data['name']
    aDict['popularity'] = data['popularity']
    return aDict
    #pass

def fetchAlbumIds(artist_id):
    """Using the Spotify API, take an artist ID and 
    returns a list of album IDs in a list
    """
    url = "https://api.spotify.com/v1/artists/" + artist_id + "/albums?market=US&album_type=album"
    req = requests.get(url)
    data = req.json()
    albumIDs = []
    for a in data['items']:
        albumIDs.append(a['id'])
    return albumIDs
    pass

def fetchAlbumInfo(album_id):
    """Using the Spotify API, take an album ID 
    and return a dictionary with keys 'artist_id', 'album_id' 'name', 'year', popularity'
    """
    url = "https://api.spotify.com/v1/albums/" + album_id
    req = requests.get(url)
    data = req.json()
    aDict = {}
    aDict['artist_id'] = data['artists'][0]['id']
    aDict['album_id'] = data['id']
    aDict['name'] = data['name']
    aDict['year'] = data['release_date'][0:4]
    aDict['popularity'] = data['popularity']
    return aDict
    pass

if __name__ == '__main__':
    artist_names = sys.argv[1:]
    artist_ids = []
    artists = []
    #f = open('playlist.csv', 'w', encoding='utf-8')
    for a in artist_names:
        artist_ids.append(fetchArtistId(a))
    edgeLists = getEdgeList(artist_ids[0], 2)
    for i in range(len(artist_ids)):
        if i == 0:
            continue
        else:
            edgeLists = combineEdgeLists(edgeLists, getEdgeList(artist_ids[i], 2))
    dg = pandasToNetworkX(edgeLists)
    for n in range(30):
        artists.append(randomCentralNode(dg))
    playlist = []
    for artist in artists:
        aname = fetchArtistInfo(artist)['name']
        albums = fetchAlbumIds(artist)
        albid = random.choice(albums)
        albname = fetchAlbumInfo(albid)['name']
        url = "https://api.spotify.com/v1/albums/" + albid + "/tracks"
        req = requests.get(url)
        data = req.json()
        trackname = random.choice(data['items'])['name']
        playlist.append((aname, albname, trackname))
    pd.DataFrame(playlist, columns=['artist_name','album_name','track_name']).to_csv('playlist.csv', index=False, encoding='utf-8')
    #f.write(unicode(fetchArtistInfo(artist)['name']) + u',' + unicode(fetchRandoms(artist)[0]) + ',' + unicode(fetchRandoms(artist)[1]))
    
        
        
        
        
        
    
