import pickle
import matplotlib.pyplot as plt

with open("metrics.pkl", "rb") as pk_file:
    history = pickle.load(pk_file)

plt.plot(history.history['loss'], label="Training Loss")
plt.plot(history.history['val_loss'], label="Testing Loss")
plt.title("Model Loss per Epoch")
plt.legend()
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.show()

plt.plot(history.history["acc"], label="Training Accuracy")
plt.plot(history.history["val_acc"], label="Testing Accruacy")
plt.legend()
plt.title("Model Accuracy per Epoch")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.show()




