import unicodecsv as csv
import matplotlib.pyplot as plt

def getBarChartData():
    #open files to read from
    f_artists = open('artists.csv') 
    f_albums = open('albums.csv')

    #initialize number of artists and albums 
    artists_rows = csv.reader(f_artists)
    albums_rows = csv.reader(f_albums)

    artists_header = artists_rows.next()
    albums_header = albums_rows.next()

    artist_names = []
    
    decades = range(1900,2020, 10)
    decade_dict = {}

    #initialize decades to 0 (1900 to 2020)
    for decade in decades:
        decade_dict[decade] = 0
    
    #get artist data
    for artist_row in artists_rows:
        if not artist_row:
            continue
        artist_id,name,followers, popularity = artist_row
        artist_names.append(name)

    #get album data
    for album_row  in albums_rows:
        if not album_row:
            continue
        artist_id, album_id, album_name, year, popularity = album_row
        for decade in decades:
            if (int(year) >= int(decade)) and (int(year) < (int(decade) + 10)):
                decade_dict[decade] += 1
                break
    
    #set x values to decades and y values to corresponding artists and albums
    x_values = decades
    y_values = [decade_dict[d] for d in decades]

    #return
    return x_values, y_values, artist_names

def plotBarChart():
    #retrieve data via getBarChartData
    x_vals, y_vals, artist_names = getBarChartData()
    
    #plot data from getBarChartData
    fig , ax = plt.subplots(1,1)

    #parameters and labels
    ax.bar(x_vals, y_vals, width=10)
    ax.set_xlabel('decades')
    ax.set_ylabel('number of albums')
    ax.set_title('Totals for ' + ', '.join(artist_names))
    
    #show graph
    plt.show()


    
