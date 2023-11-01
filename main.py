import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from pprint import pprint

scope = "playlist-modify-private"


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="", client_secret="", redirect_uri="https://www.example.com", scope=scope, show_dialog=True, cache_path="token.txt", username=""))

user_id = sp.current_user()["id"]
print(user_id)

travel_year = input("Which year would you like to travel to?  Type the data in this format YYYY-MM-DD: ")

year = travel_year.split("-")[0]

response = requests.get(f"https://www.billboard.com/charts/hot-100/{travel_year}")

soup = BeautifulSoup(response.text, "html.parser")

song_names_spans = soup.select("li ul li h3")  # This is used to zero down on particular element - you can think of this like accessing a particular folder in a tree, step by step
song_names = [song.getText().strip() for song in song_names_spans]

song_uris = []
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{travel_year} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)




