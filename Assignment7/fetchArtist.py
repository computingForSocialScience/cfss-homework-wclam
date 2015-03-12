import sys
import requests
import csv

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

#print(fetchArtistId('Beyonce'))
def fetchArtistInfo(artist_id):
    """Using the Spotify API, takes a string representing the id and
`   returns a dictionary including the keys 'followers', 'genres', 
    'id', 'name', and 'popularity'.
    """
    url = 'https://api.spotify.com/v1/artists/' + artist_id
    req = requests.get(url)
    assert req.ok, 'n/a'
    data = req.json()
    artist_info = {}
    assert data.get('name'), 'n/a'
    artist_info['followers'] = data['followers']['total']
    artist_info['genres'] = data['genres']
    artist_info['id'] = artist_id
    artist_info['name'] = data['name']
    artist_info['popularity'] = data['popularity']
    return artist_info
#print(fetchArtistInfo(fetchArtistId('Beyonce')))


