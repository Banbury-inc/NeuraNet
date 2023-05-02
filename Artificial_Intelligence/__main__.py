import requests
import json
import os
import pandas as pd
import tensorflow as tf
import subprocess
import platform
import ipfsapi


from train_model import train


def train_model():
    datasets = []
    dataset_url = "https://storage.googleapis.com/download.tensorflow.org/example_images/"
    numberofdatasets = 0


        # implementation of training a model
    while True:
        # Print menu options
        print("\nWhich type of model would you like to train?")
        print("1. Classification")
        print("2. Back")
        # Get user input
        choice = input("Enter the number of your choice: ")
    
        # Perform the selected action
        if choice == "1":
            print("\nEnter the datasets of your choice: Press enter for default(Flower Dataset)")
            while dataset_url != "0":
                dataset_url = input("Enter the datasets URL's (0 to stop)")
                if dataset_url == "":
                    dataset_url = "https://storage.googleapis.com/download.tensorflow.org/example_images/"
                if dataset_url != "0":
                    datasets.append(dataset_url)
            print("\nEpochs: Press enter for default(2)")
            epochs = input("Enter the number of epochs for this model: ")
            if epochs == "":
                epochs = 2
            else:
                epochs = int(epochs)
            print("\nImage Target Size: Press enter for default(180)")
            image_target_size = (input("Enter the image target size (ie. 180): "))
            if image_target_size == "":
                image_target_size = 180
            else:
                image_target_size = int(image_target_size)
            print("\nValidation Split: Press enter for default(180)")
            validation_split = (input("Enter the percent of the dataset you would like to use for training (and the rest for validation) (ie. .2) for this model: "))
            if validation_split == "":
                validation_split = 0.2
            else:
                validation_split = float(validation_split)  
            for i, dataset in enumerate(datasets):
                print(f"\nTraining with dataset {i+1}: {dataset}")
                train(epochs, image_target_size, validation_split, datasets)
            print("Training completed successfully")
            main()
        elif choice == "2":
            main()
        
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")
        ("Estimating listing price...")

def main():
    while True:
        # Print menu options
        print("\nWhat would you like to do?")
        print("1. Generate Inference")
        print("2. Train Model")
        print ("3. Quit")

        
        # Get user input
        choice = input("Enter the number of your choice: ")
        
        # Perform the selected action
        if choice == "1":
            generate_inference()
        elif choice == "2":
            train_model()
        elif choice == "3":
            print ("Goodbye!")
            False
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")

if __name__ == "__main__":
    main()
    
