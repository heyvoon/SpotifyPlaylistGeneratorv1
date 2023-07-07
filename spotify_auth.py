import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import session

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


def get_auth_url():
    return sp_oauth.get_authorize_url()


def get_token_info(code):
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    access_token = token_info['access_token']
    sp = spotipy.Spotify(auth=access_token)
    user_id = sp.me()['id']
    session['access_token'] = access_token
    session['user_id'] = user_id
    return token_info


def get_spotify_client():
    token_info = session.get('token_info')
    if not token_info:
        return None
    return spotipy.Spotify(auth_manager=sp_oauth)
