from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIFY_CLIENT_ID = "your spotify client id"
SPOTIFY_CLIENTS_SECRET = "your client secret"

date_needed = input("Which year do you want to travel to? Type the date in the format of YYYYMMDD:")

response = requests.get(f"https://www.officialcharts.com/charts/singles-chart/{date_needed}/")
billboard_webpage = response.text

soup = BeautifulSoup(billboard_webpage, "html.parser")
song_names_spans = soup.find_all("div", class_="title")
song_names = [song.getText() for song in song_names_spans]
print(song_names)

stripped_song_names = [i.strip("\n") for i in song_names]
print(stripped_song_names)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id= SPOTIFY_CLIENT_ID,
        client_secret= SPOTIFY_CLIENTS_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)

song_uris = []
for song in stripped_song_names:
    result = sp.search(q=f"track:{song}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


user_id = sp.current_user()["id"]

playlist = sp.user_playlist_create(user=user_id, name=f"{date_needed} TOP 100", public=False)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
