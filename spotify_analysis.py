import spotipy      # Actual api's will be accessible with this
from spotipy.oauth2 import SpotifyOAuth

def get_top_artist_names(token_info):
    sp = spotipy.Spotify(auth=token_info['access_token'])
    top_artists = sp.current_user_top_artists()["items"]
    names = [artist["name"] for artist in top_artists]
    return names

def get_top_track_names(token_info):
    sp = spotipy.Spotify(auth=token_info['access_token'])
    top_tracks = sp.current_user_top_tracks()["items"]
    names = [track["name"] for track in top_tracks]
    return names