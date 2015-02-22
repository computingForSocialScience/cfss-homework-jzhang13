import requests
import pandas as pd

#https://api.spotify.com/v1/artists/6UE7nl9mha6s8z0wFQFIZ2/related-artists

def getRelatedArtists(artistID):
    url = "https://api.spotify.com/v1/artists/" + artistID + "/related-artists"
    req = requests.get(url)
    data = req.json()
    relatedArtists = []
    for i in data['artists']:
        relatedArtists.append(i['id'])
    return relatedArtists

def getDepthEdges(artistID, depth):
    pairs = []
    if depth < 1:
        return pairs
    relArt = getRelatedArtists(artistID)
    pairs = [(artistID,j) for j in relArt]
    if depth == 1:
        return pairs
    for j in relArt:
        pairs += getDepthEdges(j, depth-1)
    return list(set(pairs))
            
def getEdgeList(artistID, depth):
    return pd.DataFrame(getDepthEdges(artistID, depth))
    
def writeEdgeList(artistID, depth, filename):
    getEdgeList(artistID, depth).to_csv(filename, index=False, encoding='utf-8')
