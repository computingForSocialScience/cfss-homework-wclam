import sys
import requests
import csv
import pandas as pd
import numpy as np

def fetchArtistId(name):
    """Using the Spotify API search method, take a string that is the artist's name, 
    and return a Spotify artist ID.
    """
    name = name.lower().replace(' ', '%20')
    url = 'https://api.spotify.com/v1/search?q=' + name + '&type=artist'
    req = requests.get(url)
    assert req.ok, 'n/a'
    data = req.json()
    assert data.get('artists').get('items'), 'n/a'
    return data['artists']['items'][0]['id']

def getRelatedArtists(artistID):
    """returns a list of related artist IDs"""
    url = "https://api.spotify.com/v1/artists/" + artistID + "/related-artists"
    req = requests.get(url)
    assert req.ok, 'n/a'
    data = req.json()
    assert data.get('artists'), 'n/a'
    return [aID['id'] for aID in data['artists']]
#print getRelatedArtists('2mAFHYBasVVtMekMUkRO9g')

def getDepthEdges(artistID, depth):
    """Takes 2 arguments, and artistID and an integer (depth)"""
    """Returns list of tuples representing pairs of related artists"""
    artist_tree = []
    searchList = getRelatedArtists(artistID)

    for a in searchList:
        tup = artistID, a
        artist_tree.append(tup)

    while depth > 0:
        for id in searchList:
            depth_list1 = []
            temp_list = getRelatedArtists(id)
            for x in temp_list:
                tup = id, x
                if tup in artist_tree:
                    pass
                else:
                    artist_tree.append(tup)
        depth = depth-1
        searchList = temp_list
    return artist_tree

#print getDepthEdges('2mAFHYBasVVtMekMUkRO9g', 1)
#print len(getDepthEdges('2mAFHYBasVVtMekMUkRO9g', 2))

def getEdgeList(artistID, depth):
    tuplelist = getDepthEdges(artistID, depth)
    edgelist = pd.DataFrame(tuplelist)
    edgelist.columns = ['artistID', 'artistID_2']
    return edgelist
#getEdgeList('2mAFHYBasVVtMekMUkRO9g', 1)

def writeEdgeList(artistID, depth, filename):
    save_edgelist = getEdgeList(artistID, depth)
    save_csv_file = save_edgelist.to_csv(filename, index = False)
writeEdgeList('2mAFHYBasVVtMekMUkRO9g', 1, 'testcsv.csv')