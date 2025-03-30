from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = str(client_id) + ":" + str(client_secret)
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"} 
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=2"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]

    if len(json_result) ==0:
        print("No artist with this name exists...")
        return None
    
    return json_result[0]

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

def get_albums_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["items"]
    return json_result

def get_artist_description(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    genres = json_result.get("genres", [])
    popularity = json_result.get("popularity", [])
    followers = json_result.get("followers", {}).get("total","N/A")
    description = f"Genres: {genres} \n" 
    description += f"Popularity: {popularity}% \n"
    description += f"Followers: {followers} followers\n"
    return description

def get_artist_image(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["images"]
    return json_result

token = get_token()

while True:    
    user_need = input("What artist would you like to know about? ")
    print(f"What would you like to know about {user_need}? Enter a Number")
    print("1. Top Tracks by Artist ")
    print("2. Albums by the Artist ")
    print("3. Description of Artist")
    print("4. Images of the Artist ")
    print("5. End Program")
    response = int(input("Enter a Number"))

    result = search_for_artist(token, user_need)
    artist_id = result["id"]

    if response == 1:
        songs = get_songs_by_artist(token, artist_id)
        for idx, song in enumerate(songs):
            print(f"{idx + 1}. {song['name']}")
    elif response == 2:
        albums = get_albums_by_artist(token, artist_id)
        for idx, album in enumerate(albums):
            print(f"{idx + 1}. {album['name']} (Released: {album['release_date']})")
    elif response == 3:
        biography = get_artist_description(token, artist_id)
        print(biography)
    elif response == 4:
        images = get_artist_image(token, artist_id)
        print(images)
    else:
        print("ending Program")
        break

    learn_more = input("Would you like to learn more about this artist (yes/no)?: ")
    if learn_more != "yes":
        print("Ending Program")
        break



