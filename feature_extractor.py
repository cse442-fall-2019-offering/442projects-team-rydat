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

        print(len(fdist))

        common = fdist.most_common(topk)
        vocab = {}
        i = 0
        for pair in common:
            vocab[pair[0]] = i
            i += 1

        vocab["UNK"] = i

        return vocab

#######################################################################################################################

    def encode_data_with_features(self, vocab):
        encoded_data = []
        for i, line in enumerate(self.input):
            newline = [vocab[word] if word in vocab else len(vocab.keys())-1 for word in word_tokenize(line)]
            encoded_data.append(newline)
            if i%10000 == 0:
                print("Encoding data: line " + str(i))

        return encoded_data

#######################################################################################################################

    def save_list_as_csv(self, vocab):

        with open("vocab.csv", "w+") as csv_file:
            wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
            for element in vocab:
                wr.writerow(element)

#######################################################################################################################

