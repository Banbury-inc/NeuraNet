import matplotlib.pyplot as plt
import numpy as np
import PIL
import tensorflow as tf
import os
import platform
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing import image
import pathlib
from pathlib import Path
import subprocess
import ipfsapi
from tensorflow.keras.models import load_model


def train(epochs, image_target_size, validation_split, datasets):
    if isinstance(datasets, str):
        datasets = [datasets]
    
    # Count the number of images in each data directory
    image_count = 0
    for dataset_url in datasets:
        if dataset_url == "https://storage.googleapis.com/download.tensorflow.org/example_images/":
            data_dir = tf.keras.utils.get_file('flower_photos', origin=dataset_url, untar=True)
            data_dir = pathlib.Path(data_dir)
        else:
            data_dir = pathlib.Path(dataset_url)
        
        image_count += len(list(data_dir.glob('*/*.jpg')))
    
    print(f'Number of images: {image_count}')

    # Load some images from the data directories
    for dataset_url in datasets:
        if dataset_url == "https://storage.googleapis.com/download.tensorflow.org/example_images/":
            data_dir = tf.keras.utils.get_file('flower_photos', origin=dataset_url, untar=True)
            data_dir = pathlib.Path(data_dir)
        else:
            data_dir = pathlib.Path(dataset_url)



    # Define some parameters for the loader
    batch_size = 32
    img_height = 180
    img_width = 180

    # create a validation split for the model. Use 80% of the images for training and 20% for validation
    train_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size)

    # create validation and use 20%
    val_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size)

    # print some of the class names 
    class_names = train_ds.class_names
    print(class_names)


    # The image_batch is a tensor of the shape (32, 180, 180, 3). 
    # This is a batch of 32 images of shape 180x180x3 (the last dimension refers to color channels RGB). 
    # The label_batch is a tensor of the shape (32,), these are corresponding labels to the 32 images.

    # configure dataset for performance
    # dataset.cache = keeps the images in memory after they're loaded off disk during the first epoch. 
    # This will ensure the dataset does not become a bottleneck while training the model. 
    AUTOTUNE = tf.data.AUTOTUNE

    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)


    # Standardize the data. The RGB channel values are in the [0, 255] range. This is not ideal for a neural network; in general you should seek to make your input values small.
    # Here, you will standardize values to be in the [0, 1] range by using tf.keras.layers.Rescaling:

    normalization_layer = layers.Rescaling(1./255)
    normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
    image_batch, labels_batch = next(iter(normalized_ds))
    first_image = image_batch[0]
    # Notice the pixel values are now in `[0,1]`.
    print(np.min(first_image), np.max(first_image))




    # Data Augmentation
    # Overfitting generally occurs when there are a small number of training examples. 
    # Data augmentation takes the approach of generating additional training data from your existing examples by augmenting them using random transformations that yield believable-looking images. 
    # This helps expose the model to more aspects of the data and generalize better.

    data_augmentation = keras.Sequential(
    [
        layers.RandomFlip("horizontal",
                        input_shape=(img_height,
                                    img_width,
                                    3)),
        layers.RandomRotation(0.1),
        layers.RandomZoom(0.1),
    ]
    )


    # Another technique to reduce overfitting is to introduce dropout regularization to the network.

    # When you apply dropout to a layer, it randomly drops out (by setting the activation to zero) a number of output units from the layer during the training process. 
    # Dropout takes a fractional number as its input value, in the form such as 0.1, 0.2, 0.4, etc. This means dropping out 10%, 20% or 40% of the output units randomly from the applied layer.
    # Create a new neural network with tf.keras.layers.Dropout before training it using the augmented images:

    model = Sequential([
    data_augmentation,
    layers.Rescaling(1./255),
    layers.Conv2D(16, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(32, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Dropout(0.2),
    layers.Flatten(),
    layers.Dense(10000, activation='relu'),
    
    ])



    # Compile and train the model
    model.compile(optimizer='adam',
                loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                metrics=['accuracy'])
    model.summary()
    epochs = epochs
    history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=epochs
    )


    # create a counter to keep track of the number of datasets generated, and 
    # write the number of datasets to a file
    
    
    # determine the value of counter based on what the number is in Number_of_Datasets.txt
    
    with open("/Users/michaelmills/Documents/GitHub/Athena/Artificial_Intelligence/Number_of_Datasets.txt", "r") as f:
        counter = int(f.read())
        counter += 1
    with open("/Users/michaelmills/Documents/GitHub/Athena/Artificial_Intelligence/Number_of_Datasets.txt", "w") as f:
        #write the value of counter to the file
        f.write(str(counter))
        f.close()
    

    # specify the directory path to create
    directory = "/Users/michaelmills/Saved_Models/"+str(counter)

    # check if directory already exists
    if not os.path.exists(directory):
        # create directory
        os.makedirs(directory)
        print(f"Directory {directory} created successfully.")
    else:
        print(f"Directory {directory} already exists.")
    
    

        
    # generate a unique file name for the saved model
    model_name = f"model_{counter}.h5"
    file_path = f"/Users/michaelmills/Saved_Models/{model_name}"

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
    with open("/Users/michaelmills/Documents/GitHub/Athena/Artificial_Intelligence/CID's.txt", "a") as f:
        f.write(f"{model_name}: {file_hash.decode()}\n")

    # Print the hash to the console
    print(f"Uploaded file '{file_path}' to IPFS with hash '{file_hash.decode()}'")

    # Stop the IPFS daemon process
    daemon_process.terminate()
    



def main():
    flowers_train_model()

if __name__ == "__main__":
    main()
