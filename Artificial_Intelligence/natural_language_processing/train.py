import numpy as np
import tensorflow_datasets as tfds
import tensorflow as tf
tfds.disable_progress_bar()
import matplotlib.pyplot as plt
import os
import sys
sys.path.append('Artificial_Intelligence')
from tensorflow.keras.layers import TextVectorization
import subprocess

url = 'Artificial_Intelligence\\natural_language_processing\\datasets'

base_dir = url


batch_size = 32
seed = 42

raw_train_ds = tf.keras.preprocessing.text_dataset_from_directory(
    base_dir,
    batch_size=batch_size,
    validation_split=0.2,
    subset='training',
    seed=seed)


raw_val_ds = tf.keras.preprocessing.text_dataset_from_directory(
    base_dir,
    batch_size=batch_size,
    validation_split=0.2,
    subset='validation',
    seed=seed)


max_features = 10000
sequence_length = 250

vectorize_layer = TextVectorization(
    max_tokens=max_features,
    output_mode='int',
    output_sequence_length=sequence_length)

# Adapt the TextVectorization layer to the training set
text_ds = raw_train_ds.map(lambda x, y: x)
vectorize_layer.adapt(text_ds)

def vectorize_text(text, label):
    text = tf.expand_dims(text, -1)
    return vectorize_layer(text), label

train_ds = raw_train_ds.map(vectorize_text)
val_ds = raw_val_ds.map(vectorize_text)


model = tf.keras.Sequential([
    tf.keras.layers.Embedding(max_features + 1, 16),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.GlobalAveragePooling1D(),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(1)])


model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              optimizer='adam',
              metrics=['accuracy'])

epochs = 50

# define a callback function to stop training when accuracy hits 90
class MyCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs={}):
        if logs.get('val_accuracy') > 0.9:
            print("\nReached 90% accuracy, so stopping training.")
            self.model.stop_training = True
            
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=epochs,
    callbacks=[MyCallback()])

# create a counter to keep track of the number of datasets generated, and 
# write the number of datasets to a file


# determine the value of counter based on what the number is in Number_of_Datasets.txt

with open("Artificial_Intelligence\\Number_of_Datasets.txt", "r") as f:
    counter = int(f.read())
    counter += 1
with open("Artificial_Intelligence\\Number_of_Datasets.txt", "w") as f:
    #write the value of counter to the file
    f.write(str(counter))
    f.close()


# specify the directory path to create
directory = "E:\Models"+str(counter)

# check if directory already exists
if not os.path.exists(directory):
    # create directory
    os.makedirs(directory)
    print(f"Directory {directory} created successfully.")
else:
    print(f"Directory {directory} already exists.")



    
# generate a unique file name for the saved model
model_name = f"model_{counter}.h5"
file_path = f"E:\\Models\\{model_name}"

# save the model to the file path
tf.keras.models.save_model(model, file_path)

# Start a new IPFS daemon process using the 'ipfs daemon' command
daemon_process = subprocess.Popen(["ipfs", "daemon"])

# Wait for the daemon to start up (optional)

# Upload the file using the 'ipfs add' command
add_output = subprocess.check_output(["ipfs", "add", "-r", file_path])

# Extract the hash of the uploaded file from the output
file_hash = add_output.split()[1]

# save the hash to CID's.txt file
with open("Artificial_Intelligence\\CID's.txt", "a") as f:
    f.write(f"{model_name}: {file_hash.decode()}\n")

# Print the hash to the console
print(f"Uploaded file '{file_path}' to IPFS with hash '{file_hash.decode()}'")

# Stop the IPFS daemon process
daemon_process.terminate()


with open("Artificial_Intelligence\\current_topic.txt", "r") as file:
    topic = file.read().strip()
print(topic)
# Open the file for appending and add the new topic
with open("Artificial_Intelligence\\topics.txt", "a") as file:
  file.write(topic + "\n")


