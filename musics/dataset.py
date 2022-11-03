import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
import environ

env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env(
    env_file='.env'
)
SPOTIPY_CLIENT_ID = env('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = env('SPOTIPY_CLIENT_SECRET')


spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

items_df = pd.DataFrame(columns=['title', 'artist', 'album', 'image', 'track_id'])

# 특정 카테고리("가요")의 플레이리스트
category_playlists = spotify.category_playlists('0JQ5DAqbMKFQtzIMjOW2bE')
for items in category_playlists['playlists']['items'] : 
    # 특정 플레이 리스트의 곡 정보
    playlist_items = spotify.playlist_items(items['id'])
    for i, items in enumerate(playlist_items['items']):
        track = [
                items['track']['name'],
                items['track']['album']['artists'][0]['name'],
                items['track']['album']['name'],
                items['track']['album']['images'][1]['url'],
                items['track']['id'],]
        items_df.loc[len(items_df)] = track

print(items_df.shape)
items_df.head()


csv_path = 'music_data.csv'
items_df.to_csv(csv_path, index=False)
