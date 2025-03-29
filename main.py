import requests
from pprint import pprint

SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player'
SPOTIFY_ACCESS_TOKEN = 'BQA9v53mEFo5txN0faebXYI6rQDHInWM1OcOVsrrY-kPeK5hMSSOB2ed2UhiophZG4IMGQAci9GCQ2o7Lr2DQ4oma-lmRkRCIJAiCnA5nec-_TpaJA6GpP1AZwK8HwEsYu473f5Qk0o'

def get_current_track(access_token):
    response = requests.get(
        SPOTIFY_GET_CURRENT_TRACK_URL,
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )
    resp_json = response.json()

    track_id = resp_json['item']['id']
    track_name = resp_json['item']['name']
    artists = resp_json['item']['artists']
    artists_names = ','.join([artist['name'] for artist in artists]
    )
    link = resp_json['item']['external_urls']['spotify']

    current_track_info = {
        "id": track_id,
        "name": track_name,
        "artists": artists_names,
        "link": link
    }

    return current_track_info

def main():
    current_track_info = get_current_track(
        SPOTIFY_ACCESS_TOKEN
    )

    pprint(current_track_info, indent=4)
     
    
if __name__ == '__main__':
    main()