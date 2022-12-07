import spotipy
from spotipy import SpotifyOAuth
from config.var_env import *

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client,
                                                    client_secret=secret,
                                                    redirect_uri=url_direct))


def get_artists_from_playlist(playlist_uri):
    """

    :param playlist_uri: Playlist to analyse
    :return: A dictionary(artist uri : artist name) of all primary artists in a playlist.
    """
    artists = {}
    playlist_tracks = spotify.playlist_tracks(playlist_id=playlist_uri)
    for song in playlist_tracks['items']:
        if song['track']:
            print(song['track']['artists'][0]['name'])
            artists[song['track']['artists'][0]['uri']] = song['track']['artists'][0]['name']
    return artists
