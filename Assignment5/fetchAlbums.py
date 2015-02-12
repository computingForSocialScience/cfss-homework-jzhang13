import requests
from datetime import datetime

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

print(fetchAlbumIds("6jJ0s89eD6GaHleKKya26X"))
print(fetchAlbumInfo(fetchAlbumIds("6jJ0s89eD6GaHleKKya26X")[0]))

