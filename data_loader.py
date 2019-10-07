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
