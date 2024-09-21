import os
import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth

# TODO-Project: Create a Spotify Playlist using WebScraping BeautifulSoup.

"""
1. Scrape the top 100 songs from a particular date.
2. Extract the song titles from the list.
3. Use the Spotify API to create a new playlist.
4. Search through Spotify, and add each of the songs to that playlist.
Once the code has completed running, Spotify would have created the new playlist.
"""

# Client Information
CLIENT_ID = os.environ["SPOTIPY_CLIENT_ID"]
CLIENT_SECRET = os.environ["SPOTIPY_CLIENT_SECRET"]
USERNAME = os.environ["USERNAME"]
REDIRECT_URL = "https://example.com/"

# User input, integrated into URL, and retrieve information in text format
data_entered = input("What year would you like to travel to? Type Date in format: YYYY-MM-DD:")
URL = f"https://www.billboard.com/charts/hot-100/{data_entered}"
response = requests.get(url=URL)
billboard = response.text

# Parse the HTML content, Retrieve Text and Remove Spaces, List Comprehension
soup = BeautifulSoup(billboard, "html.parser")
# Soup Select use of ID and class
song_titles = [title.getText().strip() for title in soup.select("li h3#title-of-a-story")]
song_artists = [artist.getText().strip() for artist in soup.select("li span.c-label.a-no-trucate")]

# Spotipy Authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URL,
                                               scope="playlist-modify-private playlist-modify-public",
                                               cache_path="token.txt",
                                               show_dialog=True,
                                               username=USERNAME))

# Retrieving ID of authenticated user
user_id = sp.current_user()["id"]

# Retrieve the Spotify URI for each artist after webscraping
# Create an empty, use for loop to loop through both lists.
spotify_uris = []
for song, artist in zip(song_titles, song_artists):
    # Query string to search Spotify's database for songs using both song title and artist name
    query = f"track:{song} artist:{artist}"
    # Search tracks using currently establishing parameters; search query,
    # type (searching for tracks), limit result to 1
    result = sp.search(q=query, type="track", limit=1)
    try:
        # Extract the URI from the search results, append to list
        uri = result["tracks"]["items"][0]["uri"]
        spotify_uris.append(uri)
    except IndexError:
        # If there is an error...
        print(f"Could not find URI for {song} by {artist}")

# Print all retrieved URIs
print(spotify_uris)

# Create a private playlist with the date entered
playlist = sp.user_playlist_create(user=user_id,
                                   name=f"{data_entered} Billboard 100",
                                   public=False,
                                   collaborative=False,
                                   description=f"Billboard Hot 100 songs for {data_entered}")
# Retrieve the playlist ID
playlist_id = playlist["id"]
# Add songs to the newly created playlist
sp.playlist_add_items(playlist_id=playlist_id, items=spotify_uris)