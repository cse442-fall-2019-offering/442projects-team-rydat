import numpy as np
import functools
import pickle

# Keras imports
from keras import Input
from keras.layers import Dense, LSTM, Bidirectional, concatenate
from keras.models import Sequential, load_model, Model
from keras.utils import to_categorical
from keras.metrics import top_k_categorical_accuracy

# Custom layer
from attention import Attention

class Emotional_Analysis_Model():

    def __init__(self, model_path, retrain=False):
        self.model_path = model_path
        self.input_size = 1 # One sequence at a time
        self.num_candidates = 5
        self.window_size = 30 # Size of sequences
        self.hidden_size = 64 # Making shit up
        self.num_hidden_layers = 1 # Making more shit up, see how it goes
        self.num_classes = 13 # Number of emotion labels
        self.num_epochs = 30 # Train for 30 epochs

        # Defines custom metric for comparing accuracy against the top k most probable predictions
        self.topk_acc = functools.partial(top_k_categorical_accuracy, k=self.num_candidates)
        self.topk_acc.__name__ = 'topk_acc'

        if retrain:
            if "attention" or "Attention" in model_path:
                self.model = self.create_Keras_model("attention")
            else:
                self.model = self.create_Keras_model("basic")
        else:
            self.model = load_model(model_path, custom_objects={"Attention":Attention, "topk_acc":self.topk_acc})

#######################################################################################################################

    def create_Keras_model(self, type):
        if type == "basic":
            model = Sequential()
            model.add(LSTM(self.window_size, return_sequences=True, input_shape=(self.window_size, self.input_size),
                           activation="relu"))

            for i in range(self.num_hidden_layers):
                model.add(LSTM(self.hidden_size, return_sequences=False, activation="relu"))

            model.add(Dense(self.num_classes, activation="softmax"))
            model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy", self.topk_acc])

            return model

        if type == "attention":
            input = Input(shape=(self.window_size, self.input_size))
            lstm = Bidirectional(LSTM(self.hidden_size,
                                      return_sequences=True,
                                      return_state=True,
                                      dropout=0.1,
                                      activation="relu"))(input)

            lstm, forward_h, forward_c, backward_h, backward_c = Bidirectional(LSTM(self.hidden_size,
                                                                                return_sequences=True,
                                                                                return_state=True,
                                                                                dropout=0.1,
                                                                                activation="relu"))(lstm)

            state_h = concatenate([forward_h, backward_h])
            context_vector = Attention(self.window_size)([lstm, state_h])
            output = Dense(self.num_classes, activation="softmax", name="output_layer")(context_vector)

            model = Model(inputs=input, outputs=output)
            model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy", self.topk_acc])

            return model

#######################################################################################################################

    def train(self, train_data, train_labels, validation_data=None, validatation_labels=None):

        if validation_data is not None:
            self.model.fit(train_data, train_labels, batch_size=128, verbose=1, epochs=self.num_epochs,
                           validation_data=(validation_data, validatation_labels))
        else:
            self.model.fit(train_data, train_labels, batch_size=128, verbose=1, epochs=self.num_epochs)

        print("Trained DeepLog model")

        self.model.save(self.model_path)
        print("Saved model as: " + self.model_path)

#######################################################################################################################

    def split_data(self, data, labels, percent_split):
        length = len(data)
        cutoff = int(percent_split * length)
        train_data = data[cutoff:]
        train_labels = labels[cutoff:]
        val_data = data[:cutoff]
        val_labels = labels[:cutoff]

        return train_data, train_labels, val_data, val_labels

#######################################################################################################################

if __name__ == '__main__':
    EAM = Emotional_Analysis_Model("first_try_attention", retrain=True)

    with open("padded_data.pkl", "rb") as pk_file:
        data = np.array(pickle.load(pk_file))
    print(data)

    with open("padded_labels.pkl", "rb") as pk_file:
        labels = pickle.load(pk_file)

    labels = to_categorical(labels, EAM.num_classes)
    data = np.reshape(data, (data.shape[0], data.shape[1], 1))
    data = data/2801

    print(data)

    train_data, train_labels, val_data, val_labels = EAM.split_data(data, labels, 0.2)

    EAM.train(train_data, train_labels, validation_data=val_data, validatation_labels=val_labels)
