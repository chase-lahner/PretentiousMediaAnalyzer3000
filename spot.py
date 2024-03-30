import os

from flask import Flask, jsonify, request, session, redirect, url_for

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)

client_id = '0d17cf42d40a48bea802aef127087548'
client_secret = '7afa8777c069421492d72d1d57de49a1'
redirect_uri = 'http://localhost:5000/callback'
scope = 'playlist-read-private user-library-read user-top-read'

cache_handler = FlaskSessionCacheHandler(session)
sp_oauth = SpotifyOAuth(client_id=client_id,
                        client_secret= client_secret,
                        redirect_uri=redirect_uri,
                        scope=scope,
                        cache_handler=cache_handler,
                        show_dialog=True)
sp = Spotify(auth_manager=sp_oauth)


@app.route('/')
def home():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return redirect(url_for('poop'))


@app.route('/homefr')
def homefr():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return "welcome to my page <a href='/get_songs'>get top_songs</a>"



@app.route('/callback')
def callback():
    sp_oauth.get_access_token(request.args['code'])
    return redirect(url_for('homefr'))


@app.route('/get_playlists')
def get_playlists():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)

    playlists = sp.current_user_playlists()
    playlists_info = [(pl['name'], pl['external_urls']['spotify'])
                      for pl in playlists['items']]
    playlists_html = '<br>'.join([f'{name}:{url}' for name, url in playlists_info])
    return playlists_html


@app.route('/get_songs')
def get_songs():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    songs = sp.current_user_top_tracks(limit=50)
    song_info = [(pl['name'], pl['artists'][0]['name'])
                for pl in songs['items']]
    songs_html = '<br>'.join([f'{name}:{artist}' for name, artist in song_info])

    return songs_html
                 
                 

    
                   
    return jsonify(songs)

    



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
    


