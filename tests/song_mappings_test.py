from login import Login
from login import NoTokenError
import spotipy
from heapq import nsmallest

loggingIn = Login()

try:
    token = loggingIn.getToken(loggingIn.REDIRECT_URI)
except NoTokenError:
    loggingIn.login()
    # Below line no longer works for some reason. Must run once, copy new URL, replace variable below and run again.
    # url = input()
    url = "https://www-student.cse.buffalo.edu/CSE442-542/2019-Fall/cse-442j/?code=AQDlxf6ELGRfTMW2DJ_lTWXkC1sBxM0W2PfZm6cRnoQvCW1CgjawzygqLt3PF7u1gXgnlCVOJ0trSHoFuS1J4GbjN_JxukvSsgBivlfMmLKwK1QzuiG0FgjgDHb7xv5DZtOvPOwJerjhRHmKwZepBG_2P8HmvOrtWCVO6UCDHCj5qMtIW1G7KFrhxoVSWNyN-lnK_6WvXxaQh7ktjmdi4tW1-k2pQT-2AoWz1oMyU-dGP2qUDxrNiSfPBZxhxQkP-jO4Lz6kt1Geh01RyYURjLiBMtWDGy6gofm4_wgxzJeLib7UJnPpht23QuSrJito-teoGM4uxRPU7WF2-ZHDCCk4IzcLqc53K2GM3YNeyuPgScyTr6RoQdK5yzaaAb30h0fh1ReeMyImP3ORAVxgzkhEaGulrRGDPZqF9ft_6EEoq2t2GA_6RxwtLftSt6-wqzAtzhCvKJkSeIYKvKsOQrf6m3htzVYFkTIO99BWDdga1sPMoCE"
    token = loggingIn.getToken(url)

sp = spotipy.client.Spotify(auth=token['access_token'])

# Get the users top 15 artists (maximum for spotipy)
results = sp.current_user_top_artists()
artistList = []
for item in results['items']:
    artistList.append(str(item["id"]))

track_names = []
track_ids = []
track_valences = []
bunches = []

# Get tracks for artists 0 - 4
recommendations = sp.recommendations(seed_artists=artistList[:5], limit=100)
for track in recommendations["tracks"]:
    track_names.append(track["name"])
    track_ids.append(track["id"])
    track_valences.append(["valence"])

# Get tracks for artists 5 - 9
recommendations = sp.recommendations(seed_artists=artistList[5:10], limit=100)
for track in recommendations["tracks"]:
    track_names.append(track["name"])
    track_ids.append(track["id"])
    track_valences.append(["valence"])

# Get tracks for artists 10 - 14
recommendations = sp.recommendations(seed_artists=artistList[10:14], limit=100)
for track in recommendations["tracks"]:
    track_names.append(track["name"])
    track_ids.append(track["id"])
    track_valences.append(["valence"])

# Get audio features of recommended tracks in groups of 50 (spotipy maximum)
# Add track names, ids, and valences to tuples
# Names are not currently used, only useful for script testing.
upper_bound = 50
for i in range(0, len(track_ids), 50):
    features = sp.audio_features(track_ids[i:upper_bound])
    upper_bound += 50
    for j, feature in enumerate(features):
        bunches.append((track_names[j], track_ids[j], feature["valence"]))

# Sort tuples by valence values
bunches = sorted(bunches, key=lambda bunch: bunch[2])

# Choose the 30 tracks with valence values closest to the sentiment value
playlist_tracks = nsmallest(30, bunches, key=lambda bunch: abs(bunch[2] - .50))

print("Prediction value: 0.50")
print(playlist_tracks)