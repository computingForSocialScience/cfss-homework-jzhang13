import sys
from fetchArtist import fetchArtistId, fetchArtistInfo
from fetchAlbums import fetchAlbumIds, fetchAlbumInfo
from csvUtils import writeArtistsTable, writeAlbumsTable
from barChart import plotBarChart

if __name__ == '__main__':
    artist_names = sys.argv[1:]
    print "input artists are ", artist_names
    artists = []
    albums = []
    for an in artist_names:
        a_id = fetchArtistId(an)
        artists.append(fetchArtistInfo(a_id))
        albs = fetchAlbumIds(a_id)
        for alb in albs:
            albums.append(fetchAlbumInfo(alb))
    writeArtistsTable(artists)
    writeAlbumsTable(albums)
    plotBarChart()

