import json
import numpy as np
import keras.preprocessing.text as kpt
import spotipy
from keras.preprocessing.text import Tokenizer
from heapq import nsmallest
from keras.models import model_from_json
import os
import sys

def convert_text_to_index_array(text):

    # read in our saved dictionary
    with open('dictionary.json', 'r') as dictionary_file:
        dictionary = json.load(dictionary_file)

    # this utility makes sure that all the words in your input
    # are registered in the dictionary
    # before trying to turn them into a matrix.
    words = kpt.text_to_word_sequence(text)
    wordIndices = []
    for word in words:
        if word in dictionary:
            wordIndices.append(dictionary[word])
        else:
            print("'%s' not in training corpus; ignoring." %(word))
    return wordIndices

def remove_appos(text):
    appos = {"aren't": "are not",
             "can't": "cannot",
             "couldn't": "could not",
             "didn't": "did not",
             "didn": "did not",
             "doesn't": "does not",
             "don't": "do not",
             "hadn't": "had not",
             "hasn't": "has not",
             "haven't": "have not",
             "he'd": "he would",
             "he'll": "he will",
             "he's": "he is",
             "i'd": "i would",
             "i'll": "i will",
             "i'm": "i am",
             "isn't": "is not",
             "it's": "it is",
             "it'll": "it will",
             "i've": "i have",
             "let's": "let us",
             "mightn't": "might not",
             "mustn't": "must not",
             "shan't": "shall not",
             "she'd": "she would",
             "she'll": "she will",
             "she's": "she is",
             "shouldn't": "should not",
             "that's": "that is",
             "there's": "there is",
             "they'd": "they would",
             "they'll": "they will",
             "they're": "they are",
             "they've": "they have",
             "we'd": "we would",
             "we're": "we are",
             "weren't": "were not",
             "we've": "we have",
             "what'll": "what will",
             "what're": "what are",
             "what's": "what is",
             "what've": "what have",
             "where's": "where is",
             "who'd": "who would",
             "who'll": "who will",
             "who're": "who are",
             "who's": "who is",
             "who've": "who have",
             "won't": "will not",
             "wouldn't": "would not",
             "you'd": "you would",
             "you'll": "you will",
             "you're": "you are",
             "you've": "you have",
             "'re": " are",
             "wasn't": "was not",
             "we'll": "we will",
             }
    words = text.lower().split()
    reformed_line = [appos[word] if word in appos else word for word in words]
    reformed = " ".join(reformed_line)
    return reformed

if __name__ == '__main__':
    if len(sys.argv) == 2:
        text_to_eval = sys.argv[1]
        token = None
    elif len(sys.argv) == 3:
        text_to_eval = sys.argv[1]
        token = sys.argv[2]
    else:
        text_to_eval = "kill me sad funeral"
        token = None

    # read in the saved model structure
    model_path = os.path.abspath("model.json")
    json_file = open(model_path, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    # and create a model from that


    model = model_from_json(loaded_model_json)
    # and weight the nodes with your saved values

    weights_path = os.path.abspath("model.h5")
    model.load_weights(weights_path)

    trimmed_sentence = remove_appos(text_to_eval)
    testArr = convert_text_to_index_array(trimmed_sentence)
    # we're still going to use a Tokenizer here, but we don't need to fit it
    tokenizer = Tokenizer(num_words=10000)
    # for human-friendly printing
    labels = ['negative', 'positive']
    input = tokenizer.sequences_to_matrix([testArr], mode='binary')
    # predict which bucket your input belongs in
    pred = model.predict(input)
    pred = pred[0][1]

    from login import Login
    from login import NoTokenError
    loggingIn =Login()

    try:
        token =loggingIn.getToken(loggingIn.REDIRECT_URI)
    except NoTokenError:
        loggingIn.login()
        # Below line no longer works for some reason. Must run once, copy new URL, replace variable below and run again.
        # url = input()
        url = "https://www-student.cse.buffalo.edu/CSE442-542/2019-Fall/cse-442j/?code=AQAVzDvWQStmE9jGd5ZuB9bEbW4kWW30oVMPlqJ8Yuf_OK3DEtVtk7xqRJImmd8QdOsON72XLmyamVjfNxfT8yJKpiV-APXb6sQRkfH8svlccnBU33bNxuHoS2-UQilbNHfNE1F9wFd04WFNK9HXCEyfuDW07B_qYrRsPqSYmWEmYO06euAhI3vgwS2-sLSAQ3mj5yPVEXAOsOHForjM-ryxPtNzPn9U8W9f5yj5ysscO782tTTCEs7zke18n9BtrM6aE7iMkwA5Tvfkj_4QldilZe5oGtI-m5tUDVHj0khex7PLeZW5HDQiq3w4aGaTt_l_LB7DjXjesz6CKWDJusPA6uG-5y2zQEF1TOGSgYgUPJbNWREo987fIL2Wg9RZ1oP63PY7SWA90Lsh2ZBS_GafDsXkwHDO3cEZ7p0AyAI66LJyFhhJBirlvmC7dIeR762eA-SMySPIEx9EAT1vCW5y5HJuLGONI35qN5m1-Bd3hQhfI5U"
        token =loggingIn.getToken(url)

    sp =spotipy.client.Spotify(auth=token['access_token'])

    # Get the users top 15 artists (maximum for spotipy)
    results =sp.current_user_top_artists()
    artistList =[]
    for item in results['items']:
        artistList.append(str(item["id"]))

    track_names = []
    track_ids = []
    bunches = []

    # Get tracks for artists 0 - 4
    recommendations = sp.recommendations(seed_artists=artistList[:5], limit=100)
    for track in recommendations["tracks"]:
        track_names.append(track["name"])
        track_ids.append(track["id"])

    # Get tracks for artists 5 - 9
    recommendations = sp.recommendations(seed_artists=artistList[5:10], limit=100)
    for track in recommendations["tracks"]:
        track_names.append(track["name"])
        track_ids.append(track["id"])

    # Get tracks for artists 10 - 14
    recommendations = sp.recommendations(seed_artists=artistList[10:14], limit=100)
    for track in recommendations["tracks"]:
        track_names.append(track["name"])
        track_ids.append(track["id"])

    # Get audio features of recommended tracks in groups of 50 (spotipy maximum)
    # Add track names, ids, and valences to tuples
    # Names are not currently used, only useful for script testing.
    upper_bound = 50
    for i in range(0, len(track_ids), 50):
        features = sp.audio_features(track_ids[i:upper_bound])
        upper_bound += 50
        for j, feature in enumerate(features):
            bunches.append((track_names[j], feature["id"], feature["valence"]))

    # Choose the 30 tracks with valence values closest to the sentiment value
    playlist_tracks = nsmallest(30, bunches, key=lambda bunch: abs(bunch[2] - pred))
    #print(pred)
    #for bunch in playlist_tracks:
        #print(bunch)

    # Create a new playlist
    playlist = sp.user_playlist_create(sp.me()["id"], text_to_eval, public=True)

    # Get the ID for future use
    playlist_id = playlist["id"]

    # Determine the list of track IDs to add to the playlist
    good_ids = set()
    for track in playlist_tracks:
        good_ids.add(track[1])

    # Add tracks
    sp.user_playlist_add_tracks(sp.me()["id"], playlist_id, good_ids)

