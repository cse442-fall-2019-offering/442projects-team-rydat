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
                      "didn" : "did not",
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
    """ Separates a phrase into a list of separate words, called tokens
    
        Takes in data line by line
    """

    def tokenize(self, line):
        tokens = nltk.tokenize.word_tokenize(line)
        return tokens

#######################################################################################################################

    """ Converts a line to lowercase, removes all hashtags and mentions"""

    def normalize(self, line):
        # Step 1: convert line to lowercase
        lowercase = line.lower()

        # Step 2: remove apostrophes
        words = lowercase.split()
        reformed_line = [self.appos[word] if word in self.appos else word for word in words]
        reformed = " ".join(reformed_line)

        # Step 3: Fucking hashtags and @'s
        words = reformed.split()
        better = ["" if "#" in word or "@" in word else word for word in words]
        return " ".join(better)

#######################################################################################################################

    """ Removes all punctuation from a phrase, only keeps alphabetical characters """

    def remove_punctuation(self, tokens):
        words = [word for word in tokens if word.isalpha()]
        return words

#######################################################################################################################

    """ General process for cleaning data. Goes through normalization step, then passed to gensim lemmatize funtion """

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
            if i%10000 == 0:
                print("Cleaning data: line " + str(i))

        return self.separate_tags_n_words(tags_n_words)

#######################################################################################################################

    """ Separates words from their part-of-speech tag """

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

    """ Adds 0's to the end of a sequence to make sure that each sequence is the same length.
        Also encodes labels into numerical form
     
        Only used for sequence model
    """

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



#######################################################################################################################

    """ Enocdes labels for Bag of Words model 
        Throws out any data lines with less than 3 words
        
    """


    def encode_labels(self, vectorized_data):
        #if len(self.label_encodings.keys()) == 0:
        #    self.get_label_encodings()
        encoded = []
        for i, line in enumerate(vectorized_data):
            if i%10000 == 0:
                print("Checking lengths: line " + str(i))
            if sum(line) < 3:
                vectorized_data.remove(line)
            else:
        #        encoded.append((line, self.label_encodings[self.labels[i]]))
                encoded.append((line, self.labels[i]))
        return encoded

#######################################################################################################################

    """ Determines the possible label encodings from all labels 
        Ex. 13 possible emotions get mapped to 13 labels.
    """

    def get_label_encodings(self):
        possible_labels = set()
        for label in self.labels:
            possible_labels.add(label)
        for i, label in enumerate(possible_labels):
            self.label_encodings[label] = i

#######################################################################################################################

    """ Converts dataset in bag of words vector representation, where each value in the vector represents
        how many times that particular word appears in the data line.
        
        Only used for bag of words model.
    """

    def prep_bag_of_words(self, vocabulary, data):
        words = vocabulary.keys()
        v_size = len(words)
        vectorized_data = []
        for i, line in enumerate(data):
            if i % 10000 == 0:
                print("Bagging words: line " + str(i))
            vectorized_data.append([0]*(v_size))
            for word in words:
                vectorized_data[i][vocabulary[word]] = line.count(vocabulary[word])

        return vectorized_data


#######################################################################################################################

    def reduce_by_label(self, acceptable_labels):
        reduced_labels = []
        reduced_data = []
        for i, line in enumerate(self.data):
            if self.labels[i] in acceptable_labels:
                reduced_data.append(line)
                reduced_labels.append(self.labels[i])

        self.labels = reduced_labels
        self.data = reduced_data

 ######################################################################################################################
