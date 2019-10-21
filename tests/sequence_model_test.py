import pickle
import numpy as np
from emotional_analysis_model import Emotional_Analysis_Model

with open("../processed_data/BOW_big_data.pkl", "rb") as pk_file:
    data = np.array(pickle.load(pk_file))

with open("../processed_data/BOW_big_labels.pkl", "rb") as pk_file:
    labels = pickle.load(pk_file)

with open("../processed_data/vocabulary.pkl", "rb") as pk_file:
    vocab = dict(pickle.load(pk_file))

EAM = Emotional_Analysis_Model("binary_seq", input_size=len(vocab.keys()), retrain=True)

labels = np.divide(labels, 4)
print(labels)
# labels = to_categorical(labels, 2)
#data = np.reshape(data, (data.shape[0], data.shape[1], 1))
data = np.divide(data, len(vocab.keys()))

# print(data)

train_data, train_labels, val_data, val_labels = EAM.split_data(data, labels, 0.2)

EAM.train(train_data, train_labels, validation_data=val_data, validatation_labels=val_labels)