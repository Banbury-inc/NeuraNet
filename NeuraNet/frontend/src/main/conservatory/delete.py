import logging
from flask import Flask,request, jsonify
import sys
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
import os
import socket
from dotenv import load_dotenv
import configparser
import json


# Get the home directory of the user
home_directory = os.path.expanduser("~")
# Specify the folder for Banbury Cloud-related files
BANBURY_FOLDER = os.path.join(home_directory, ".banbury")

# Specify the full path to the configuration file
CONFIG_FILE = os.path.join(BANBURY_FOLDER, ".banbury_config.ini")

# Ensure the configuration file exists; create it if it doesn't
if not os.path.exists(CONFIG_FILE):
    # Create a ConfigParser instance with default values
    config = configparser.ConfigParser()
    config["banbury_cloud"] = {
        "credentials_file": "credentials.json"
    }
    
    # Write the configuration to the file
    with open(CONFIG_FILE, "w") as config_file:
        config.write(config_file)


def load_credentials():
    try:
        # Create a ConfigParser instance and read the configuration file
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        credentials_file = config.get("banbury_cloud", "credentials_file")

        # Example: Load credentials from the specified file
        credentials_file_path = os.path.join(BANBURY_FOLDER, credentials_file)
        with open(credentials_file_path, "r") as file:
            return json.load(file)

    except (configparser.Error, FileNotFoundError):
        return {}



def connect_to_relay_server():
    load_dotenv()
    RELAY_HOST = "34.28.13.79" 
    RELAY_PORT = 8002

    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sender_socket.connect((RELAY_HOST, RELAY_PORT))
    return sender_socket



def delete_file(files, device):

    credentials = load_credentials()

    username = next(iter(credentials))    

    file_path = files

    file_name = file_path

    sender_socket = connect_to_relay_server()

    print(f"File Name: {file_name}")
    file_size = ""
    file_header = f"FILE_DELETE_REQUEST:{file_name}:{file_size}:{username}:"
    sender_socket.send(file_header.encode())
    sender_socket.send(b"END_OF_HEADER") # delimiter to notify the server that the header is done

    return

def main():

    if len(sys.argv) == 2:
        files = sys.argv[1]
        device = "default"
        print(f"Argument received: {files}")
    if len(sys.argv) == 3:
        files = sys.argv[1]
        device = sys.argv[2]
        print(f"Argument received: {files}" + " " + f"Device: {device}")
 
    else:
        print("No argument received.")
        files = "welcome.txt"
        device = "default"
    delete_file(files, device)

if __name__ == '__main__':
    main()

