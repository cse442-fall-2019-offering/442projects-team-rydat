import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth as OAuth
import webbrowser

''' this module allows users to login to the main page
    and either gets or provides a token to allow access to
    a users spotify information
'''


class NoTokenError(Exception):
    """ there exists no token currently cached on this account"""
    pass

class Login:
    
    def __init__(self):
        ''' sets redirect page to the home page'''
        self.REDIRECT_URI = 'https://www-student.cse.buffalo.edu/CSE442-542/2019-Fall/cse-442j/'
        '''these are rob's client\secret Ids'''
        self.clientId='c00c658f3a8a4a29961ae9fe70ffde7e'
        self.Secret='e3fbfba45325459cb7b3b408f41f3a12'
        self.scope='user-read-email user-top-read playlist-read-private user-library-read user-read-playback-state user-read-currently-playing streaming user-read-private user-modify-playback-state'
        self.authentication=(OAuth(self.clientId,self.Secret,self.REDIRECT_URI,state=None,scope=self.scope))
    
    ''' checks to see if there is already a token in the system if not
        check the  if there is one URL to see if there is one in the url'''
    def getToken(self,url=None):
            token=self.authentication.get_cached_token()
            if token is not None:
                return token
            else:
                if url is not None:
                    try:
                        return self.authentication.get_access_token(self.authentication.parse_response_code(url))
                    except  spotipy.oauth2.SpotifyOauthError:
                        raise NoTokenError
                else:    
                    raise NoTokenError
    ''' this will be the method called when the connect with spotify button is pressed
        on the login screen
        if loggedOut is true it will show dialogue for having a user log back in
        '''        
    def login(self,loggedOut=False):
        dialogue=""
        if(loggedOut is True):
            dialogue="&show_dialog=true"
        webbrowser.open(self.authentication.get_authorize_url()+dialogue)
    
    ''' function will redirect to the authorization page and give option
        to login in as a new user'''
    def logout(self, token):
        token=None
        self.login(True)                