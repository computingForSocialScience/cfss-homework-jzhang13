import csv
import sys
import numpy as np
import matplotlib.pyplot as plt

LAT_INDEX = 128
LONG_INDEX = 129 
ZIP_CODES = [28,35,42,49,56,63,70,77,84,91,98,105,112,119,126]

def readCSV(filename):
    '''Reads the CSV file `filename` and returns a list
    with as many items as the CSV has rows. Each list item 
    is a tuple containing the columns in that row as stings.
    Note that if the CSV has a header, it will be the first
    item in the list.'''
    with open(filename,'r') as f:
        rdr = csv.reader(f)
        lines = list(rdr)
    return(lines)

### enter your code below

def get_avg_latlng():
    mydata = readCSV('permits_hydepark.csv')
    lendata = len(mydata)
    totallat = 0
    totallong = 0
    for i in range(lendata):
        if mydata[i][LAT_INDEX] != '':
            totallat = totallat + float(mydata[i][LAT_INDEX])
        if mydata[i][LONG_INDEX] != '':
            totallong = totallong + float(mydata[i][LONG_INDEX])
    avglat = totallat / lendata
    avglong = totallong / lendata
    print 'avg latitude is ' + str(avglat)
    print 'avg longitude is ' + str(avglong)

def zip_code_barchart():
    mydata = readCSV('permits_hydepark.csv')
    lendata = len(mydata)
    codes = {}
    for i in range(lendata):
        for j in ZIP_CODES:
            if mydata[i][j] != '':
                key = mydata[i][j]
                if key in codes:
                    codes[key] = codes[key] + 1
                else:
                    codes[key] = 1
    zips = []
    for k in sorted(codes.keys()):
        zips.append(codes[k])
    ziplen = len(codes.keys())
    index = np.linspace(0, ziplen, ziplen)
    w = 0.9
    x,ax = plt.subplots()
    ax.bar(index, zips, w)
    ax.set_xlabel('Hyde Park Zip Codes')
    ax.set_ylabel('Zip Codes')
    ax.set_xticklabels(zips)
    plt.savefig('chart.jpg')
        
def main():
    if len(sys.argv) <= 1:
        print "error no arg"
    elif sys.argv[1] == 'latlng':
        get_avg_latlng()
    elif sys.argv[1] == 'hist':
        zip_code_barchart()
    else:
        print "error invalid arg"
    
main()
