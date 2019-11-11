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
        self.REDIRECT_URI = 'http://localhost:8000/home/'
        self.clientId='9f78b7eb1de54f6eb13701d07a891506'
        self.Secret='563e75870871424f9a26bb2bb66897bb'
        self.scope='user-read-email user-top-read playlist-modify-public user-library-read user-read-playback-state user-read-currently-playing streaming user-read-private user-modify-playback-state'
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
    def logout(self, token=None):
        token=None
        self.login(True)
if __name__== "__main__":
    loggingIn=Login()
    try:
        token=loggingIn.getToken(loggingIn.REDIRECT_URI)
    except NoTokenError:
        loggingIn.login()
        print("please enter the url in the redirected page")
        url=input()
        token=loggingIn.getToken(url)



    print("\n"+str(token))

    ''' for testing purpose the tester will have to manually input the redirect uri
        but in the application should be handled by framework '''

    print("\n here is the user information:\n")
    sp=spotipy.client.Spotify(auth=token['access_token'])
    print(str(sp.current_user()))


    print("\n here are the user's top artists:\n")
    results=sp.current_user_top_artists()
    artistList=[]
    for item in results['items']:
        artistList.append(str(item['name']))
    print(str(artistList))
    print("\n here are the user's top tracks:\n")
    results=sp.current_user_top_tracks()
    for item in results['items']:
        songList=[]
        for artist in item['artists']:
            songList.append(artist['name'])
        print(str(item['name'])+" from: "+str(item['album']['name'])+" by "+str(songList))


    print("\n\n testing that logging out provides a new token")
    print("\noriginal token:\n"+str(token['access_token'])+"\n")
    print("\n press enter to logout")
    input()
    loggingIn.logout(token)
    print("please enter the url in the redirected page")
    url=input()
    token=loggingIn.getToken(url)
    print("\nnewtoken:\n"+str(token['access_token'])+"\n")
