#Intergration
import tkinter as tk
from tkinter import scrolledtext, font
from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import webbrowser

#Client ID and secret
load_dotenv() 
'''Loads the .env file'''  

client_id = os.getenv("CLIENT_ID") 
'''obtains the client ID fom the .env file''' 
client_secret = os.getenv("CLIENT_SECRET") 
'''obtains the client secret fom the .env file''' 

#Obtaining an Access Token/API key from the spotify API
def get_token():
    auth_string = str(client_id) + ":" + str(client_secret)
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    '''Takes and links the client ID and client secret and encodes using a base64 encoding, send to API to recieve access token/API key'''

    url = "https://accounts.spotify.com/api/token"
    '''Where the request is called called from'''

    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    '''Send in our authorisation data, where it will verify that everything is correct, send back acess token/API key'''

    data = {"grant_type": "client_credentials"} 
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token
'''Ultises a json to extract data the access token and raises and error if it was unsuccessful '''

#Header Construction
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}
'''constructs a header each time by sending a request to the API '''

#Search function for a speafic type of artist
def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=2"
    '''Searchs for an artist name by requesting from the APU'''
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    '''Extracts the data from the access token from the API for the artist name'''

    if len(json_result) ==0:
        print("No artist with this name exists...")
        return None
    '''Outputs if artist doesn't exists'''
    return json_result[0]

#Function for Top tracks by artist
def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=AU"
    '''Where the request is called called from'''
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result
"Extracts data from the API for the Top tracks of the Artist"

#Function for Albums by artist
def get_albums_by_artist(token, artist_id):
    '''Where the request is called called from'''
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums?country=AU"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["items"]
    return json_result
"Extracts data from the API for the Albums of the Artist"

#Function for descripition of artist
def get_artist_description(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    '''Where the request is called called from'''
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
"Extracts data from the API in the format of genres, popularity and followers"

#Function for images of artist
def get_artist_image(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    '''Where the request is called called from'''
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["images"]
    return json_result
'''Extracts data from the API for the images of the artist'''

#GUI Display
#Creating the Tkinter Application
root = tk.Tk() 
root.title("Spotify Artist API") 
root.configure(bg='#191414') 
'''Creates the name of the GUI and changes the colour of the background'''

#Obtains the access token
token = get_token() 

#Function for search for an artist
def search_artist(): 
    artist_name = artist_name_searchbar.get()
    artist_info = search_for_artist(token, artist_name)
    artist_id = artist_info["id"]
    artist_data = {
        "name": artist_info["name"],    
        "id": artist_id
    }
    '''retrieves and search the request from the API, specifically for the name and id'''
    artist_details_frame.pack(fill="x", expand=True)
    '''creates a frame for the artist details to be visible'''


#Command Panel
    top_tracks_button.config(command=lambda:display_top_tracks(artist_id))
    '''takes the specfic function (top tracks) and displays it on the GUI when its called'''
    albums_button.config(command=lambda: display_albums(artist_id))
    '''takes the specfic function (albums) and displays it on the GUI when its called'''
    artist_descripition_button.config(command=lambda: display_description(artist_id))
    '''takes the specfic function (descripition) and displays it on the GUI when its called'''
    artist_images_button.config(command=lambda: display_images(artist_id))
    '''takes the specfic function (images) and displays it on the GUI when its called'''
    exit_button.config(command=root.destroy)
    '''takes the specfic function (exit) and displays it on the GUI when its called'''
    help_button.config(command=help)
    '''takes the specfic function (help) and displays it on the GUI when its called'''    
#Types of font
custom_font = font.Font(family="Roman", size=14)
title_font = font.Font(family="Roman", size=25)

#Artist Search Displays
title = tk.Label(root, text="Spotify Artist API", font=title_font, fg='green')
title.pack(padx=10, pady=20)
'''Display a label with the name of the GUI'''
artist_name = tk.Label(root, text="Enter Artist Name:", font=custom_font, fg='green')
artist_name.pack(padx=10)
'''Display a label asking for an artist name'''
artist_name_searchbar = tk.Entry(root, width=40, font=custom_font, fg='green')
artist_name_searchbar.pack(padx=10, pady=10)
'''Displays a searchbar for the user to enter an artist name'''
search_button = tk.Button(root, text="Search Artist", command=search_artist, font=custom_font, fg='green')
search_button.pack(padx=10, pady=10)
'''Displays a button for the GUI to make a request to the API for the data'''

#Functions for displaying the data
#Function for displaying top tracks by artist
def display_top_tracks(artist_id):                                     
    tracks = get_songs_by_artist(token, artist_id)
    result_text.delete(1.0, tk.END)
    for idx, track in enumerate(tracks):
        result_text.insert(tk.END, f"{idx + 1}. {track['name']}\n")
'''Extracts the data from the API and displays the top tracks by the artist in the GUI'''

#Function for displaying albums by artist
def display_albums(artist_id):
    albums = get_albums_by_artist(token, artist_id)
    result_text.delete(1.0, tk.END)
    for idx, album in enumerate(albums):
        result_text.insert(tk.END, f"{idx + 1}. {album['name']} (Released: {album['release_date']})\n")
'''Extracts the data from the API and displays the albums by the artist in the GUI'''

#Function for displaying descripition of artist
def display_description(artist_id):
    description = get_artist_description(token, artist_id)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, description)
'''Extracts the data from the API and displays the description of the artist in the GUI'''

#Function for displaying the images of artist
def display_images(artist_id):
    images = get_artist_image(token, artist_id)
    result_text.delete(1.0, tk.END)
    for img in images:
        result_text.insert(tk.END, f"Image URL: {img['url']}\n")
        webbrowser.open_new(img['url'])
'''Extracts the data from the API and displays the description of the artist in the GUI'''

#Function for exiting the program
def exit():
    root.destroy()
'''Forces the program the end and close'''

#Function for help
def help():
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "This is the help menu, here are a few methods you could try\n")
    result_text.insert(tk.END, "1. Restart the program\n")
    result_text.insert(tk.END, "2. Enter another artist/track name\n")
    result_text.insert(tk.END, "3. Check the Internet Connection\n")
    result_text.insert(tk.END, "4. Update Software\n")
    result_text.insert(tk.END, "3. Check Authorization\n")
    result_text.insert(tk.END, "If none of these methods work, please feel free to contact the developer\n")
    return None
'''Displays a bunch of text with help incase the user encounters an issue'''

#Button Display for each function
artist_details_frame = tk.Frame(root)
'''Creates a frame for the buttons'''
top_tracks_button = tk.Button(artist_details_frame, text="Top Tracks by Artist", font=custom_font, fg='green')
top_tracks_button.pack(padx=10, pady=5)
'''Displays a button when click calls the API for a request to display the top tracks by the artist on the GUI'''
albums_button = tk.Button(artist_details_frame, text="Albums by Artist", font=custom_font, fg='green')
albums_button.pack(padx=10, pady=5)
'''Displays a button when click calls the API for a request to display the albums by the artist on the GUI'''
artist_descripition_button = tk.Button(artist_details_frame, text="Description of Artist", font=custom_font, fg='green')
artist_descripition_button.pack(padx=10, pady=5) 
'''Displays a button when click calls the API for a request to display a description of the artist on the GUI'''
artist_images_button= tk.Button(artist_details_frame, text="Images of Artist", font=custom_font, fg='green')
artist_images_button.pack(padx=10, pady=5)
'''Displays a button when click calls the API for a request to display images of the artist on the GUI'''
exit_button= tk.Button(artist_details_frame, text="Exit", font=custom_font, fg='red')
exit_button.pack(padx=10, pady=5)
exit_button.place(x=10, y=10)
'''Displays an exit button when click forces the GUI to end and close'''
help_button= tk.Button(artist_details_frame, text="Help", font=custom_font, fg='blue')
help_button.pack(padx=10, pady=5)
help_button.place(x=10, y=50)
'''Displays an help button when click displays a bunch of options which could resolves issues with the GUI'''

#Data Output
result_text = scrolledtext.ScrolledText(root, width=100, height=15)
result_text.pack(padx=10, pady=10)
"After the User press on of the buttons, an API request is called and the data is displayed here"

#GUI
root.mainloop()
"runs the GUI"

