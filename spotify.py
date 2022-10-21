import requests
import time

from pprint import pprint


SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player/currently-playing'
ACCESS_TOKEN = 'BQBRaGdEOnnbnvmertTDBWWIqMCZfdPpQG6OXUg3udvCtBNjuNSuBuf_HYIM67QXInn8GFQUYquQ8eAxtA6xiyfp_hCNpVPcBi_R1gSZlqnStzYRzz39ynEEB2ZosfyhFc7MV3WOGJ4jSm1AHj-cV2PiyyzGzxaUJKQptatR9Q-uXk5EQ13GpoD0jeqsSsOsI_9D'


def get_current_track():
    response = requests.get(
        SPOTIFY_GET_CURRENT_TRACK_URL,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {ACCESS_TOKEN}"
        }
    )
    if response.status_code not in [204, 404]:
        json_resp = response.json()
        track_id = json_resp['item']['id']
        track_name = json_resp['item']['name']
        artists = [artist for artist in json_resp['item']['artists']]
        artists_names = ''
        for artist in artists:
            artists_names +=  artist['name'] + ', '
        return {
            'track_id': track_id,
            'track_name': track_name,
            'artists': artists_names[:-2]

        }
    
    else: 
        return "No track playing"




