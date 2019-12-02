import sys
import os
import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2
import urllib
import requests

scope = 'user-read-email user-top-read playlist-modify-public user-library-read user-read-playback-state user-read-currently-playing streaming user-read-private user-modify-playback-state'
client_id = '9f78b7eb1de54f6eb13701d07a891506'
client_secret = '563e75870871424f9a26bb2bb66897bb'
redirect_uri = 'http://www.mooduse.live:8000/home/'
cache_path = None
state = None
sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, state, scope, cache_path)

def rob_login(logout=False):
    dialog = ""
    if(logout is True):
        dialog="&show_dialog=true"
    auth_url = sp_oauth.get_authorize_url()+dialog
    response = urllib.request.urlopen(auth_url).geturl()
    return response

def rob_logout(token=None):
    token_info = None
    return rob_login(True)
