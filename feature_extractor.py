from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
import csv

class Extractor():
    def __init__(self, input):
        self.input = input

#######################################################################################################################

    def get_features(self, topk):

        # Good vocab size for just twitter data is 2800
        fdist = FreqDist()
        for line in self.input:
            for word in word_tokenize(line):
                fdist[word] += 1

        common = fdist.most_common(topk)
        vocab = {}
        for i, pair in enumerate(common):
            vocab[pair[0]] = i+1

        return vocab

#######################################################################################################################

    def encode_data_with_features(self, vocab):
        encoded_data = []
        for line in self.input:
            newline = [vocab[word] if word in vocab else 2801 for word in word_tokenize(line)]
            encoded_data.append(newline)

        return encoded_data

#######################################################################################################################

    def save_list_as_csv(self, vocab):

        with open("vocab.csv", "w+") as csv_file:
            wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
            for element in vocab:
                wr.writerow(element)