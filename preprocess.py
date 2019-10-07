from data_loader import Loader
from feature_extractor import Extractor
from gensim.utils import lemmatize
import pandas as pd
import pickle
import nltk
import numpy as np

"""
Dict of common appostrophe phrases found on analytics vidhy blog user comments:
https://www.analyticsvidhya.com/blog/2014/11/text-data-cleaning-steps-python/
"""

class Preprocess():
    def __init__(self, data, labels):
        self.max_length = 30
        self.data = data
        self.labels = list(labels)
        self.label_encodings = {}
        self.appos = {"aren't" : "are not",
                      "can't" : "cannot",
                      "couldn't" : "could not",
                      "didn't" : "did not",
                      "doesn't" : "does not",
                      "don't" : "do not",
                      "hadn't" : "had not",
                      "hasn't" : "has not",
                      "haven't" : "have not",
                      "he'd" : "he would",
                      "he'll" : "he will",
                      "he's" : "he is",
                      "i'd" : "I would",
                      "i'll" : "I will",
                      "i'm" : "I am",
                      "isn't" : "is not",
                      "it's" : "it is",
                      "it'll":"it will",
                      "i've" : "I have",
                      "let's" : "let us",
                      "mightn't" : "might not",
                      "mustn't" : "must not",
                      "shan't" : "shall not",
                      "she'd" : "she would",
                      "she'll" : "she will",
                      "she's" : "she is",
                      "shouldn't" : "should not",
                      "that's" : "that is",
                      "there's" : "there is",
                      "they'd" : "they would",
                      "they'll" : "they will",
                      "they're" : "they are",
                      "they've" : "they have",
                      "we'd" : "we would",
                      "we're" : "we are",
                      "weren't" : "were not",
                      "we've" : "we have",
                      "what'll" : "what will",
                      "what're" : "what are",
                      "what's" : "what is",
                      "what've" : "what have",
                      "where's" : "where is",
                      "who'd" : "who would",
                      "who'll" : "who will",
                      "who're" : "who are",
                      "who's" : "who is",
                      "who've" : "who have",
                      "won't" : "will not",
                      "wouldn't" : "would not",
                      "you'd" : "you would",
                      "you'll" : "you will",
                      "you're" : "you are",
                      "you've" : "you have",
                      "'re": " are",
                      "wasn't": "was not",
                      "we'll":"we will",
}
#######################################################################################################################

    def tokenize(self, line):
        tokens = nltk.tokenize.word_tokenize(line)
        return tokens

#######################################################################################################################

    def normalize(self, line):
        # Step 1: convert line to lowercase
        lowercase = line.lower()

        # Step 2: remove apostrophes
        words = lowercase.split()
        reformed_line = [self.appos[word] if word in self.appos else word for word in words]
        reformed = " ".join(reformed_line)

        # Step 3: Fucking hashtags and @'s
        words = lowercase.split()
        better = ["" if "#" in word or "@" in word else word for word in words]
        return " ".join(better)

#######################################################################################################################

    def remove_punctuation(self, tokens):
        words = [word for word in tokens if word.isalpha()]
        return words

#######################################################################################################################

    def clean_data(self):
        tags_n_words = []
        for i, line in enumerate(self.data):
            # Step 1: Decode the data into utf-8 format
            #decoded = line.decode("utf-8-sig")

            # Step 2: Normalize (lowercase and apostrophe conversion)
            normal = self.normalize(line)

            # Step 3: Lemmatize
            lemma = lemmatize(normal)
            tags_n_words.append(lemma)

        return self.separate_tags_n_words(tags_n_words)

#######################################################################################################################

    def separate_tags_n_words(self, tags_n_words):
        words = []
        tags = []
        for row in tags_n_words:
            sent = []
            type = []
            for word in row:
                split = word.decode().split('/')
                sent.append(split[0])
                type.append(split[1])
            words.append(" ".join(word for word in sent))
            tags.append(" ".join(word for word in type))

        return words

#######################################################################################################################

    def pad_sequences(self, encoded_data):
        if len(self.label_encodings.keys()) == 0:
            self.get_label_encodings()
        padded = []
        for i, line in enumerate(encoded_data):
            if len(line) > self.max_length or len(line) == 0:
                continue
            else:
                while len(line) < self.max_length:
                    line.append(0)
                padded.append((line, self.label_encodings[self.labels[i]]))

        return padded

#######################################################################################################################

    def get_label_encodings(self):
        possible_labels = set()
        for label in self.labels:
            possible_labels.add(label)
        for i, label in enumerate(possible_labels):
            self.label_encodings[label] = i

#######################################################################################################################



if __name__ == '__main__':

    loader = Loader("raw_data")
    train_data, train_labels = loader.read_twitter_data("twitter_text_emotion.csv")

    preprocess = Preprocess(train_data, train_labels)

    clean = preprocess.clean_data()

    extractor = Extractor(clean)
    vocab = extractor.get_features(2800)
    encoded = extractor.encode_data_with_features(vocab)
    padded_pairs = preprocess.pad_sequences(encoded)
    padded_data = []
    padded_labels = []
    for pair in padded_pairs:
        padded_data.append(pair[0])
        padded_labels.append(pair[1])

    with open("padded_data.pkl", "wb") as pk_file:
        pickle.dump(padded_data, pk_file)

    with open("padded_labels.pkl", "wb") as pk_file:
        pickle.dump(padded_labels, pk_file)