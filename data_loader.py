import pandas as pd

class Loader():

    def __init__(self, data_directory):
        self.directory = data_directory

    def read_twitter_data(self, file_path):
        data_frame = pd.read_csv(self.directory + "/" + file_path)
        train_data = data_frame["content"]
        train_labels = data_frame["sentiment"]
        return (train_data, train_labels)

    def read_plutchik_data(self, file_path):
        data_frame = pd.read_csv(self.directory + "/" + file_path)
        train_data = data_frame["sentence"]
        train_labels = data_frame["emotion"]
        return (train_data, train_labels)

    def read_biggle(self, file_path):
        data_frame = pd.read_csv(self.directory + "/" + file_path, encoding= "ISO-8859-1")
        sample = data_frame.sample(frac=0.05)
        train_data = sample.iloc[: , 5]
        train_labels = sample.iloc[:, 0]
        print(train_labels)
        return (train_data, train_labels)