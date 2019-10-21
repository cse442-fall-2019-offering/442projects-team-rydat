from login import Login
from login import NoTokenError
import spotipy

loggingIn = Login()

try:
    token = loggingIn.getToken(loggingIn.REDIRECT_URI)
except NoTokenError:
    loggingIn.login()
    # Below line no longer works for some reason. Must run once, copy new URL, replace variable below and run again.
    # url = input()
    url = "https://www-student.cse.buffalo.edu/CSE442-542/2019-Fall/cse-442j/?code=AQBQr2EIaeS2ZE2qz-UoBGERXHF8Ege9HSqKvlRk6qEpTz-2tgZS7wHYpmI2l2x8UBw5jKz59LdH0CXl5LgYrZVHLRc1kOUmgAEepF4AqQBBZ1f-woqZ_nQmRp2Ojg-9ApSeVd-ADoDiABgwZ2wY6_u3N6nJK7U6qvoFSUw2jOPl_cWh7uzmXjQG6SFtnqAlAevQmlUiDchAdFwbhJsrAQzOexIVbTU9SJn7YiI8f3d0I-3mT6vlG0v3e2aCnkLczpHcRthpjYv6UuugZecly3Q_8H66pPeKKuPcm6F2iyuTN8kzmUptJlV-VBIP3jM3qcowTWOLgaQwmYXTTSipYTDHyuVnxSqzntFKtJna5lvYE08H99eGz_pqgOT7G9ThhlJAaZbeaZS-VkCDm6fsZ9EbDrXf0RtxVaU-juNZ_Iblz3j5N2ZZcwIeSRWjBqUrHPJRo_jHAys1a0ppQ5MAXJFW9GrAKDxG4k3KPspLpvYKglc7HGw"
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
print("Songs sorted by valence values")
for i in range(len(bunches)):
    print(bunches[i][0])
    print(bunches[i][2])
    print("")