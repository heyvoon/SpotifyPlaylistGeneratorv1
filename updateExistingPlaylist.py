import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables from .env file
load_dotenv()

# Set variables from environment variables
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

scope = "playlist-modify-private user-library-read"

sp_oauth = SpotifyOAuth(client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET,
                        redirect_uri=REDIRECT_URI,
                        scope=scope)

auth_url = sp_oauth.get_authorize_url()
print(f"Please navigate here: {auth_url}")

response = input("Enter the URL you were redirected to: ")
code = sp_oauth.parse_response_code(response)
token_info = sp_oauth.get_access_token(code)

sp = spotipy.Spotify(auth_manager=sp_oauth)

# Define the list of DJs
djs = [
    "Bandbewerbungen",
    "Presse",
    "Kulturkosmos",
    "Kontakt",
    "Impressum",
    "Datenschutz",
    # Add more DJs as needed
]

# Set the ID of the playlist to update
playlist_id = "6UYhcXeljOmxWVf3yCg3mu"

# Search for albums by each DJ and add their tracks to the playlist
for dj in djs:
    results = sp.search(q=f"artist:{dj}", type="album", limit=1)
    if results["albums"]["items"]:
        album_uri = results["albums"]["items"][0]["uri"]
        tracks = sp.album_tracks(album_uri)
        track_uris = [track["uri"] for track in tracks["items"]]
        sp.playlist_add_items(playlist_id, track_uris)
    else:
        print(f"No albums found for DJ '{dj}' on Spotify.")