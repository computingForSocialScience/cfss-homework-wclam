import unicodecsv as csv
import matplotlib.pyplot as plt

def getBarChartData():
    f_artists = open('artists.csv')
    f_albums = open('albums.csv') #These both open the files 


    artists_rows = csv.reader(f_artists) 
    albums_rows = csv.reader(f_albums) #these read the files in a row

    artists_header = artists_rows.next() 
    albums_header = albums_rows.next() #this gets the headers

    artist_names = []  #this creates a new list for the collected data to be put in
    
    decades = range(1900,2020, 10)  #this is a range counter from 1900-2020 separated by 10 year intervals
    decade_dict = {}  #this a dictionary for counting 
    for decade in decades:
        decade_dict[decade] = 0 #fills the dictionary with data
    
    for artist_row in artists_rows: #loops through the data looking for the artist names
        if not artist_row: #check to see if this row is the header
            continue
        artist_id,name,followers, popularity = artist_row  #gets the value
        artist_names.append(name) #adds name to the list

    for album_row  in albums_rows: #loops through the data looking for the album names
        if not album_row: #checks to see if this is the header
            continue
        artist_id, album_id, album_name, year, popularity = album_row #get values from row
        for decade in decades: #iterate all of the decades in the range
            if (int(year) >= int(decade)) and (int(year) < (int(decade) + 10)): #check if the data is in that decade
                decade_dict[decade] += 1 #if it is, count it
                break

    x_values = decades  #get a list of decades
    y_values = [decade_dict[d] for d in decades] #get a list of number of albums corresponding to the given decade
    return x_values, y_values, artist_names

def plotBarChart():  #gets data from getBarChartData in order to plot a graph
    x_vals, y_vals, artist_names = getBarChartData() #get data
    
    fig , ax = plt.subplots(1,1)  #format of the graph
    ax.bar(x_vals, y_vals, width=10) #barchart function
    ax.set_xlabel('decades') #set the xlabel
    ax.set_ylabel('number of albums') #set the ylabel
    ax.set_title('Totals for ' + ', '.join(artist_names)) #set the graph title
    plt.show() #show the graph