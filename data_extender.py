import spotipy
import csv
import sys
from dotenv import dotenv_values
from spotipy.oauth2 import SpotifyClientCredentials

arguments = sys.argv
start = int(arguments[1])
end = int(arguments[2])

env_vars = dotenv_values('.env')

CLIENT_ID = env_vars.get('SPOTIFY_APP_ID')
CLIENT_SECRET = env_vars.get('SPOTIFY_APP_SECRET')

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID,
                                                           client_secret=CLIENT_SECRET))

input_file = 'charts.csv'
output_file = 'charts_extended.csv'

with open(input_file, 'r') as csv_input_file:
    reader = csv.reader(csv_input_file)
    rows = list(reader)

rows[0].extend(['acousticness', 'danceability', 'duration_ms', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'tempo', 'genre'])

for i, row in enumerate(rows[1:], start=start):
    print(i, row[2])
    artist = row[3]
    if('Featuring' in artist):
        artist = row[3].split('Featuring')[0]
    if('&' in artist):
        artist = row[3].split('&')[0]
    if(' x ' in artist):
        artist = row[3].split(' x ')[0]
    if('(' in artist):
        artist = row[3].split(' (')[0]
    track = row[2]
    result = sp.search(q=f"artist:{artist} track:{track}", type="track", limit=1)
    if(result['tracks']['total'] == 0):
        result = sp.search(q=f"track:{track}", type="track", limit=1)
    if(result['tracks']['total'] != 0):
        track_id = result['tracks']['items'][0]['id']
        audio_features = sp.audio_features(tracks=[track_id])[0]
        row.append(audio_features['acousticness'])
        row.append(audio_features['danceability'])
        row.append(audio_features['duration_ms'])
        row.append(audio_features['energy'])
        row.append(audio_features['instrumentalness'])
        row.append(audio_features['liveness'])
        row.append(audio_features['speechiness'])
        row.append(audio_features['tempo'])
        artists = result['tracks']['items'][0]['artists']
        genre = []
        for artist in artists:
            genre.extend(sp.artist(artist['id'])['genres'])
        row.append(';'.join(genre))
    if(i==end):
        break

with open(output_file, 'w', newline='') as csv_output_file:
    writer = csv.writer(csv_output_file)
    writer.writerows(rows[start:end])
    