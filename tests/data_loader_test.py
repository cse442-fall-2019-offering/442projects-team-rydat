from data_loader import Loader

loader = Loader("raw_data")
(train_data, train_label) = loader.read_twitter_data("twitter_text_emotion.csv")
print("Size of training data:")
print(train_data.shape)
print("")
print(train_data[5])
print(train_label[5])
print("")
print(train_data[100])
print(train_label[100])
print("")
print(train_data[250])
print(train_label[250])