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



def delete_file(device_name):

    credentials = load_credentials()
    username = next(iter(credentials))    
    sender_socket = connect_to_relay_server()
    print(f"Device Name: {device_name}")
    file_size = ""
    null_arg = ""
    file_header = f"DEVICE_DELETE_REQUEST:{device_name}:{null_arg}:{username}:"
    sender_socket.send(file_header.encode())
    sender_socket.send(b"END_OF_HEADER") # delimiter to notify the server that the header is done

    return

def main():

    if len(sys.argv) > 1:
        device_name = sys.argv[1]
        print(f"Argument received: {device_name}")
    else:
        print("No argument received.")
        device_name = "michael-GF65-Thin-9SD"

    delete_file(device_name)

if __name__ == '__main__':
    main()

