import spotipy
from dotenv import dotenv_values
from spotipy.oauth2 import SpotifyClientCredentials

env_vars = dotenv_values('.env')

CLIENT_ID = env_vars.get('SPOTIFY_APP_ID')
CLIENT_SECRET = env_vars.get('SPOTIFY_APP_SECRET')

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID,
                                                           client_secret=CLIENT_SECRET))

results = sp.search(q='weezer', limit=20)
for idx, track in enumerate(results['tracks']['items']):
    print(idx, track['name'])
                                    