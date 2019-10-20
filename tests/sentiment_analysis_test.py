import json
import numpy as np
import keras.preprocessing.text as kpt
import spotipy
from keras.preprocessing.text import Tokenizer
from keras.models import model_from_json
import os
import sys
from playlist_creator import *

def convert_text_to_index_array(text):

    # read in our saved dictionary
    with open('../dictionary.json', 'r') as dictionary_file:
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

text_to_eval = "How well does it work?"

# read in the saved model structure
model_path = os.path.abspath("../model.json")
json_file = open(model_path, 'r')
loaded_model_json = json_file.read()
json_file.close()
# and create a model from that


model = model_from_json(loaded_model_json)
# and weight the nodes with your saved values

weights_path = os.path.abspath("../model.h5")
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
print(text_to_eval)
print("Sentiment Score:")
print(pred)