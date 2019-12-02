import spotipy
from spotify.login_page import NoTokenError
import sys
def Mooduseplaylists(token):
    if(token is None):
        raise NoTokenError
    
    sp= spotipy.Spotify(auth=token)        
    playlists=sp.current_user_playlists(limit=50)['items']
    MoodLists=[]
    for item in playlists:
        if item['name'].find("MooDuse") != -1:
            MoodLists.append((item['name'],item['images'][1]['url'],item['id']))
    return MoodLists

if __name__ == "__main__":
    print("Enter Token:")
    token= input()
    playlists=Mooduseplaylists(token)
    for item in playlists:
        print(item)