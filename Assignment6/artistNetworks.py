import sys
import requests
import csv
import pandas as pd

#https://api.spotify.com/v1/artists/6UE7nl9mha6s8z0wFQFIZ2/related-artists

def getRelatedArtists(artistID):
    url = "https://api.spotify.com/v1/artists/" + artistID + "/related-artists"
    req = requests.get(url)
    data = req.json()
    relatedArtists = []
    for (i in data['artists']):
        relatedArtists.append(i['id'])
    return relatedArtists

def getDepthEdges(artistID, depth):
    pairs = []
    relArt = getRelatedArtists(artistID)
    if depth == 0:
        return pairs
    for j in relArt:
        pairs.append((artistID,j))
        pairs += getDepthEdges(j, depth-1)
    return list(set(pairs))
            
def getEdgeList(artistID, depth):
    return pd.DataFrame(getDepthEdges(artistID, depth))
    
def writeEdgeList(artistID, depth, filename):
    f = open(filename, 'w', encoding='utf-8')
    getEdgeList(artistID, depth).to_csv(filename, index=False)

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

print(fetchArtistId("Taylor Swift"))
print(fetchArtistInfo(fetchArtistId("Taylor Swift")))

