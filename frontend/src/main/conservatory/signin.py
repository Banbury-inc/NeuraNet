import sys
import os
import socket
from dotenv import load_dotenv
import pymongo
import getpass
import bcrypt
from pymongo.server_api import ServerApi
import hashlib
import configparser
import json




# Get the home directory of the user
home_directory = os.path.expanduser("~")
# Specify the folder for Banbury Cloud-related files
BANBURY_FOLDER = os.path.join(home_directory, ".banbury")

# Ensure the .banbury folder exists; create it if it doesn't
if not os.path.exists(BANBURY_FOLDER):
    os.makedirs(BANBURY_FOLDER)
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


def save_credentials(credentials):

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    credentials_file = config.get("banbury_cloud", "credentials_file")
    credentials_file_path = os.path.join(BANBURY_FOLDER, credentials_file)
    with open(credentials_file_path, "w") as file:
        json.dump(credentials, file)



def login(username, password_str):


    password_bytes = password_str.encode('utf-8')  # Encode the string to bytes
    load_dotenv()
    uri = os.getenv("MONGODB_URL")
    client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
    client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
    credentials = load_credentials()
    db = client['myDatabase']
    user_collection = db['users']
    user = user_collection.find_one({'username': username})
    if user and bcrypt.checkpw(password_bytes, user['password']):
        print("Login successful!")
        credentials = load_credentials()
        hashed_password = hashlib.sha256(password_str.encode()).hexdigest()
        credentials[username] = hashed_password
        save_credentials(credentials)
        
    else:
        print("Login unsuccessful!")

def main():

    if len(sys.argv) > 1:
        username = sys.argv[1]
        password_str = sys.argv[2]
        login(username, password_str)


    else:
        print("No argument received.")
        files = "chamonix.mp4"


if __name__ == '__main__':
    main()

