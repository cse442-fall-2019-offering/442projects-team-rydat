import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from playlist import Mooduseplaylists
from login import Login

l = Login()

print("You will first need  to get an Oauth token from Spotify")
print("press enter to open the redirect page")
l.login()
print("copy and paste entire url from the redirect for the token:")
token= l.getToken(input())['access_token']
print("valid token\n\n")
playlists=Mooduseplaylists(token)

print("press enter to see the playlists")
input()
for item in playlists:
    print(item[0])

print("\nverify that theese are the Mooduse Generated playlists")