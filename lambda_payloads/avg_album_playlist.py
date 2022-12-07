import csv
import spotipy
from spotipy import SpotifyOAuth
from config.spotify_playlist import spotify_playlist
from tools.playlist import get_artists_from_playlist
from config.var_env import client, secret, url_direct
import os
from pathlib import Path
import boto3
from datetime import *

spotipy_object = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client,
                                                           client_secret=secret,
                                                           redirect_uri=url_direct))

PLAYLIST = 'rap_caviar'
dir = Path(__file__).resolve().parent.parent
data = f"{dir}/data/"


def gather_data_local():
    # For every artist we're looking for
    final_data_dictionary = {
        'Year Released': [],
        'Album Length': [],
        'Album Name': [],
        'Artist': []
    }
    with open(os.path.join(f"{data}/rapcaviar_albums.csv"), 'w') as file:
        header = list(final_data_dictionary.keys())
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        albums_obtained = []

        artists = get_artists_from_playlist(spotify_playlist()[PLAYLIST])

        # for artist in artists.keys():
        for artist in list(artists.keys()):
            print(artist)
            artists_albums = spotipy_object.artist_albums(artist, album_type='album', limit=50)
            # For all of their albums
            for album in artists_albums['items']:
                if 'GB' and 'US' in album['available_markets']:
                    key = album['name'] + album['artists'][0]['name'] + album['release_date'][:4]
                    if key not in albums_obtained:
                        albums_obtained.append(key)
                        album_data = spotipy_object.album(album['uri'])
                        # For every song on the album
                        album_length_ms = 0
                        for song in album_data['tracks']['items']:
                            album_length_ms = song['duration_ms'] + album_length_ms
                        writer.writerow({'Year Released': album_data['release_date'][:4],
                                         'Album Length': album_length_ms,
                                         'Album Name': album_data['name'],
                                         'Artist': album_data['artists'][0]['name']})
                        final_data_dictionary['Year Released'].append(album_data['release_date'][:4])
                        final_data_dictionary['Album Length'].append(album_length_ms)
                        final_data_dictionary['Album Name'].append(album_data['name'])
                        final_data_dictionary['Artist'].append(album_data['artists'][0]['name'])

    return final_data_dictionary


def gether_data():
    # For every artist we re-looking for
    with open(f"{data}/rapcaviar_albums.csv", "w") as file:
        header = ['Year Released', 'Album Length', 'Album Name', 'Artist']
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        artists = get_artists_from_playlist(spotify_playlist()[PLAYLIST])
        for artist in artists.keys():
            artists_albums = spotipy_object.artist_albums(artist, album_type='album', limit=50)
            # For all of their albums
            for album in artists_albums['items']:
                if 'GB' in artists_albums['items'][0]['available_markets']:
                    album_data = spotipy_object.album(album['uri'])
                    # For every song on the album
                    album_length_ms = 0
                    for song in album_data['tracks']['items']:
                        # TODO consider album popularity
                        album_length_ms = song['duration_ms'] + album_length_ms
                    writer.writerow({'Year Released': album_data['release_date'][:4],
                                     'Album Length': album_length_ms,
                                     'Album Name': album_data['name'],
                                     'Artist': album_data['artists'][0]['name']})
    s3_resources = boto3.resource('s3')
    dates = datetime.now()
    filename = f'{dates.year}-{dates.month}-{dates.day}/rapcaviar_albums.csv'
    response = s3_resources.Object(Bucket='spotify-analysis-data1', key=filename).upload_file(
        f'{data}/rapcaviar_albums.csv')

    return response


def lambda_handler(event, context):
    gether_data()


if __name__ == '__main__':
    data = gether_data()
    # s3_resource = boto3.resource('s3')
    # dates = datetime.now()
    # filename = f'{dates.year}-{dates.month}-{dates.day}/rapcaviar_albums.csv'
    # s3_resource.Object('spotify-analysis-data1', key=filename).upload_file(f'{data}rapcaviar_albums.csv')
