import sys
sys.path.insert(0, '../mockupwebpage')
from login import Login
from login import NoTokenError
import spotipy

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

print("\n press enter to  continue")
input()

print("\n here are the user's top artists:\n")
results=sp.current_user_top_artists()
artistList=[]
for item in results['items']:
    artistList.append(str(item['name']))
print(str(artistList))

print("\n press enter to  continue")
input()

print("\n here are the user's top tracks:\n")
results=sp.current_user_top_tracks()

for item in results['items']:
    songList=[]
    for artist in item['artists']:
        songList.append(artist['name'])
    print(str(item['name'])+" from: "+str(item['album']['name'])+" by "+str(songList))
        
print("\n press enter to  continue")
input()

print("\n\n testing that logging out provides a new token upon re-authenticating")
print("\noriginal token:\n"+str(token['access_token'])+"\n")
print("\n press enter to logout")
input()
loggingIn.logout(token)
print("please enter the url in the redirected page")
url=input()    
token=loggingIn.getToken(url)
print("\nnewtoken:\n"+str(token['access_token'])+"\n")
    