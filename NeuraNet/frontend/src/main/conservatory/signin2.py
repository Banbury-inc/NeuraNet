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


def connect_to_relay_server():
    load_dotenv()
    RELAY_HOST = os.getenv("RELAY_HOST")
    RELAY_PORT = 443

    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sender_socket.connect((RELAY_HOST, RELAY_PORT))
    return sender_socket



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

    null_arg = ""
    sender_socket = connect_to_relay_server()
    header = None
    end_of_header = b"END_OF_HEADER"
    buffer = b""
    file_header = f"LOGIN_REQUEST:{null_arg}:{password_str}:{username}:"
    sender_socket.send(file_header.encode())
    sender_socket.send(b"END_OF_HEADER") # delimiter to notify the server that the header is done

    job_completed = False
    while job_completed == False:
        data = sender_socket.recv(4096)
        if not data:
            break
        buffer += data
        file_type = "Unknown"
        if end_of_header in buffer and header is None:
            header_part, content = buffer.split(end_of_header, 1)
            header = header_part.decode() 
            split_header = header.split(":")
            file_type = split_header[0]
            buffer = content 


        if file_type == "LOGIN_SUCCESS":
            job_completed = True
            result = "success"
            hashed_password = hashlib.sha256(password_str.encode()).hexdigest()
            credentials = load_credentials()
            credentials[username] = hashed_password
            save_credentials(credentials)
            sender_socket.close()

            return result
        elif file_type == "LOGIN_FAIL":
            job_completed = True
            result = "fail"
            sender_socket.close()
            return result
 





def main():

    if len(sys.argv) > 1:
        username = sys.argv[1]
        password_str = sys.argv[2]
        result = login(username, password_str)
        print(f"Result: {result}")    

    else:
        print("No argument received.")
if __name__ == '__main__':
    main()

