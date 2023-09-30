# Flask runs on http://127.0.0.1:5000, so when creating app put redirect uri as: http://127.0.0.1:5000
# You need to do an oauth, and it's easy to acesss web from python while using flask.

import spotipy      # Actual api's will be accessible with this
from spotipy.oauth2 import SpotifyOAuth     # Only for the oauth

# Basic flask requirements to set connectivity with the web
from flask import Flask, request, url_for, session, redirect

import os       # Access .env
from dotenv import load_dotenv      # get dotenv
import time     # To refresh token

load_dotenv()

app = Flask(__name__)   # create flask instance

# Create and configure session
app.config['SESSION_COOKIE_NAME'] = os.getenv("SESSION_COOKIE_NAME")
app.secret_key = os.getenv("SECRET_KEY")

TOKEN_INFO = ''       # Will be changed to actual token info


@app.route('/')         # If homepage, login
def login():
    # create_spotify_oauth() returns the OAuth then we authorize the url and redirect there
    auth_url = create_spotify_oauth().get_authorize_url()
    return redirect(auth_url)


@app.route('/redirect')
def redirect_page():
    # After Auth is created, store in session, redirect to main function,
    # After successful authentication and consent,
    # the authorization server redirects the user's browser back to your application's specified redirect URI.
    # Along with this redirection, it includes an 'authorization code' as a query parameter in the URL.
    session.clear()
    code = request.args.get('code')
    token_info = create_spotify_oauth().get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('main', external=True))


@app.route('/Analysis')
def main():
    # Check if token is existing, else redirect to login page and then do the main part
    try:
        token_info = get_token()
    except:
        print("User not logged in")
        return redirect('/')

    # Start implementation here
    return ("OAUTH SUCESSFUL")


def get_token():
    # Returns the token for the auth for this session, if not existing, return to login
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        redirect(url_for('login', external=False))

    # Check if token is expired, refresh the token
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if (is_expired):
        spotify_oauth = create_spotify_oauth()
        token_info = spotify_oauth.refresh_access_token(
            token_info['refresh_token'])

    return token_info


def create_spotify_oauth():
    # creates a spotify auth with client id, secrect; redirect to function redirect_page(); define the scopes accesible to the project
    return SpotifyOAuth(client_id=os.getenv('CLIENT_ID'),
                        client_secret=os.getenv('CLIENT_SECRET'),
                        redirect_uri=url_for('redirect_page', _external=True),
                        scope='user-library-read playlist-modify-public playlist-modify-private')  # Change this based on implementation


# Run the app
app.run(debug=True)
