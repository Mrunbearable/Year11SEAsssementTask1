import tkinter as tk
from tkinter import messagebox, scrolledtext, font
from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import webbrowser

load_dotenv()

client_id = os.getenv("CLIENT_ID") #Gets the client ID from spotify website
client_secret = os.getenv("CLIENT_SECRET") #Gets the

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

root = tk.Tk() #Creates the Tkinter program
root.title("Spotify Artist API") #Creates the name of the Tkinter Program
root.configure(bg='#191414') #Changes the colour of the background

token = get_token() #Gets Access Token

def search_artist(): #Function For Searching Artist
    artist_name = artist_name_searchbar.get()
    artist_info = search_for_artist(token, artist_name)
    artist_id = artist_info["id"]
    artist_data = {
        "name": artist_info["name"],    
        "id": artist_id
    }
    artist_details_frame.pack(fill="x", expand=True)

    top_tracks_button.config(command=lambda:display_top_tracks(artist_id))
    albums_button.config(command=lambda: display_albums(artist_id))
    artist_descripition_button.config(command=lambda: display_description(artist_id))
    artist_images_button.config(command=lambda: display_images(artist_id))
    exit_button.config(command=root.destroy)

custom_font = font.Font(family="Roman", size=14)
title_font = font.Font(family="Roman", size=25)

title = tk.Label(root, text="Spotify Artist API", font=title_font, fg='green')
title.pack(padx=10, pady=20)
artist_name = tk.Label(root, text="Enter Artist Name:", font=custom_font, fg='green')
artist_name.pack(padx=10)
artist_name_searchbar = tk.Entry(root, width=40, font=custom_font, fg='green')
artist_name_searchbar.pack(padx=10, pady=10)
search_button = tk.Button(root, text="Search Artist", command=search_artist, font=custom_font, fg='green')
search_button.pack(padx=10, pady=10)

def display_top_tracks(artist_id):                                     
    tracks = get_songs_by_artist(token, artist_id)
    result_text.delete(1.0, tk.END)
    for idx, track in enumerate(tracks):
        result_text.insert(tk.END, f"{idx + 1}. {track['name']}\n")

def display_albums(artist_id):
    albums = get_albums_by_artist(token, artist_id)
    result_text.delete(1.0, tk.END)
    for idx, album in enumerate(albums):
        result_text.insert(tk.END, f"{idx + 1}. {album['name']} (Released: {album['release_date']})\n")

def display_description(artist_id):
    description = get_artist_description(token, artist_id)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, description)

def display_images(artist_id):
    images = get_artist_image(token, artist_id)
    result_text.delete(1.0, tk.END)
    for img in images:
        result_text.insert(tk.END, f"Image URL: {img['url']}\n")
        webbrowser.open_new(img['url'])

def exit():
    root.destroy()

artist_details_frame = tk.Frame(root)
top_tracks_button = tk.Button(artist_details_frame, text="Top Tracks of Artist", font=custom_font, fg='green')
top_tracks_button.pack(padx=10, pady=5)
albums_button = tk.Button(artist_details_frame, text="Albums by Artist", font=custom_font, fg='green')
albums_button.pack(padx=10, pady=5)
artist_descripition_button = tk.Button(artist_details_frame, text="Description of Artist", font=custom_font, fg='green')
artist_descripition_button.pack(padx=10, pady=5) 
artist_images_button= tk.Button(artist_details_frame, text="Images of Artist", font=custom_font, fg='green')
artist_images_button.pack(padx=10, pady=5)
exit_button= tk.Button(artist_details_frame, text="Exit", font=custom_font, fg='red')
exit_button.pack(padx=10, pady=5)

result_text = scrolledtext.ScrolledText(root, width=100, height=15)
result_text.pack(padx=10, pady=10)
root.mainloop()


