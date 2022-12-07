import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config.var_env import client, secret, url_direct


def main():
    scope = 'user-library-read'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client,
                                                   client_secret=secret,
                                                   redirect_uri=url_direct,
                                                   scope=scope))

    results = sp.current_user_saved_tracks()
    for idx, item in enumerate(results['items']):
        track = item['track']
        print(idx, track['artists'][0]['name'], " - ", track['name'])


if __name__ == '__main__':
    main()
