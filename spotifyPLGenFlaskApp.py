import os
from flask import Flask, request, render_template, flash, redirect, url_for, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
import requests
import json
import spotipy

# Import models and spotify_auth module
from models import db, User
import spotify_auth

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Set up database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db.init_app(app)
with app.app_context():
    db.create_all()

# Set up Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Define Playlist creation function


def create_spotify_playlist(access_token, user_id, name, description):
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "name": name,
        "description": description
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 201:
        print(f"Successfully created playlist with name: {name}")
    else:
        print(f"Failed to create playlist. Response: {response.text}")


@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if not session.get('token_info'):
        auth_url = spotify_auth.get_auth_url()
        return redirect(auth_url)
    else:
        return render_template('select.html')


@app.route('/create-playlist')
def create_playlist():
    # Add your code here to handle creating a new playlist
    return render_template('create_playlist.html')


@app.route('/create-playlist-submit', methods=['POST'])
def create_playlist_submit():
    name = request.form['name']
    description = request.form['description']
    token_info = session.get('token_info')
    if spotify_auth.sp_oauth.is_token_expired(token_info):
        token_info = spotify_auth.sp_oauth.refresh_access_token(
            token_info['refresh_token'])
        session['token_info'] = token_info
    access_token = token_info['access_token']
    sp = spotipy.Spotify(auth=access_token)
    user_id = sp.me()['id']
    create_spotify_playlist(access_token, user_id, name, description)
    return redirect(url_for('index'))

@app.route('/update-playlist')
def update_playlist():
    # Add your code here to handle updating an existing playlist
    return render_template('update_playlist.html')


@app.route('/callback')
def callback():
    code = request.args.get('code')
    success = spotify_auth.get_token_info(code)
    if success:
        flash("Authorization successful!")
    else:
        flash("Authorization failed.")
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists.')
            return redirect(url_for('register'))
        user = User(username=username,
                    password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(
            f"Received login form submission with username: {username} and password: {password}")
        user = User.query.filter_by(username=username).first()
        if not user:
            print(f"No user found with username: {username}")
        elif not check_password_hash(user.password, password):
            print(f"Invalid password for user with username: {username}")
        else:
            print(f"Successfully authenticated user with username: {username}")
            login_user(user)
            flash('Login successful!')
            return redirect(url_for('index'))
    return render_template('login.html')


if __name__ == '__main__':
    app.run()