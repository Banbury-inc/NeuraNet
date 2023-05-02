import requests
import json
import os
import pandas as pd
import tensorflow as tf
import subprocess
import platform
import ipfsapi
import time

import ipfshttpclient


from flowers_train_model import flowers_train_model

def main():
    
    # Path to the file to upload
    file_path = "/Users/michaelmills/Saved_Models/flower_model"

    # Start a new IPFS daemon process using the 'ipfs daemon' command
    daemon_process = subprocess.Popen(["ipfs", "daemon"])

    # Wait for the daemon to start up (optional)
    # This gives the daemon time to start up and start listening for requests
    # If you don't wait, you might get a 'connection refused' error
    # Alternatively, you can add a time delay using the 'time.sleep()' function
    # or check if the daemon is running using the IPFS API before proceeding
    

    # sleep for 5 seconds
    time.sleep(10)
    

    # Upload the file using the 'ipfs add' command
    add_output = subprocess.check_output(["ipfs", "add", "-r", file_path])

    # Extract the hash of the uploaded file from the output
    file_hash = add_output.split()[1]

    # Print the hash to the console
    print(f"Uploaded file '{file_path}' to IPFS with hash '{file_hash.decode()}'")

    # Stop the IPFS daemon process
    daemon_process.terminate()
 

if __name__ == "__main__":
    main()
    
