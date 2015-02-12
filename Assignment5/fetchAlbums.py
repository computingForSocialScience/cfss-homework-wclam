import requests
from datetime import datetime

def fetchAlbumIds(artist_id):
    """Using the Spotify API, take an artist ID and 
    returns a list of album IDs in a list
    """
    url = 'https://api.spotify.com/v1/artists/' + artist_id + '/albums?market=US&album_type=album'
    req = requests.get(url)
    assert req.ok, 'n/a'
    data = req.json()
    assert data.get('items'), 'n/a'
    return [album['id'] for album in data['items']]

#print(fetchAlbumIds('6vWDO969PvNqNYHIOW5v0m'))    

def fetchAlbumInfo(album_id):
    """Using the Spotify API, take an album ID 
    and return a dictionary with keys 'artist_id', 'album_id' 'name', 'year', popularity'
    """
    url = 'https://api.spotify.com/v1/albums/' + album_id
    req = requests.get(url)
    assert req.ok, 'n/a'
    data = req.json()
    album_info = {}
    assert data.get('name'), 'n/a'
    album_info['artist_id'] = data['artists'][0]['id']
    album_info['album_id'] = album_id
    album_info['name'] = data['name']
    album_info['year'] = data['release_date'][0:4]
    album_info['popularity'] = data['popularity']
    return album_info
#print(fetchAlbumInfo('2UJwKSBUz6rtW4QLK74kQu'))


