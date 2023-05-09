import numpy as np
import tensorflow_datasets as tfds
import tensorflow as tf
tfds.disable_progress_bar()
import matplotlib.pyplot as plt
import os
import sys
from transformers import TFGPT2LMHeadModel, GPT2Tokenizer
import tensorflow as tf
sys.path.append('Artificial_Intelligence')
from tensorflow.keras.layers import TextVectorization
import subprocess

# load the pre-trained GPT-2 model and tokenizer
model = TFGPT2LMHeadModel.from_pretrained('gpt2')
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

# compile the model
model.compile(
    optimizer=tf.keras.optimizers.Adam(),
    loss='categorical_crossentropy',  # specify the loss function
    metrics=['accuracy']
)
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
model_name = f"model_{counter}"
file_path = f"E:\\Models\\{model_name}"

# save the model to the file path
model.save(file_path)

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

