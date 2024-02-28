import os
import shutil
import requests
import socket
import re
import argparse
import getpass
import hashlib
from dotenv import load_dotenv
import json
import pymongo
import paramiko
from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient
import bcrypt
from tabulate import tabulate
import subprocess
from datetime import datetime
import configparser
''' 
This script can be run from the command line, providing avalues for --option1 and --option2 as needed. For example:

python main.py --option1 value1 --option2 value2
'''


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
    RELAY_PORT = os.getenv("RELAY_PORT")

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


def register():
    username = input("Enter a username: ")
    load_dotenv()
    uri = os.getenv("MONGODB_URL")
    client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
    db = client['myDatabase']
    user_collection = db['users']
    credentials = load_credentials()
    user = user_collection.find_one({'username': username})
    if user: 
        print("Username already exists. Please choose another one.")
    else:
        password_str = getpass.getpass("Enter password: ")
        password_bytes = password_str.encode('utf-8')  # Encode the string to bytes
        firstName = input("Enter a first name: ")
        lastName = input("Enter a last name: ")
      
        hashed_password = hashlib.sha256(password_str.encode()).hexdigest()
        credentials[username] = hashed_password
        save_credentials(credentials)
        # Create a new user document with additional fields set to null
        new_user = {
            "username": username,
            "password": hashed_password,
            "first_name": firstName,
            "last_name": lastName,
            "phone_number": None,
            "email": None,
            "devices": [],
            "files": []
        }
        try:
            user_collection.insert_one(new_user)
            message = f"User '{username}' added successfully."
        except pymongo.errors.OperationFailure as e:
            message = f"An error occurred: {e}"

def login():
    username = input("Enter a username: ")
    password_str = getpass.getpass("Enter password: ")
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

def list_files():
    credentials = load_credentials()
    load_dotenv()
    uri = os.getenv("MONGODB_URL")
 
    client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
    username = next(iter(credentials))    
    db = client['myDatabase']
    user_collection = db['users']
    user = user_collection.find_one({'username': username})
    if not user:
        print("Please login first.")
    else:
        if user['username'] in credentials:
            try:
                files = user["files"]
                if files:
                    headers = files[0].keys()
                    rows = [list(item.values()) for item in files]
                    # Display the data in a tabular format
                    print(tabulate(rows, headers=headers, tablefmt='rounded_grid'))
                else:
                    print("No files found for this user")
            except Exception as e:
                print(f"Error displaying files:L {e}")
        else:
            print("No username found. Please register or login.")

def download_file(file_number_or_cid):
    # Search for the file with the given file number in MongoDB
    load_dotenv()
    uri = os.getenv("MONGODB_URL")
 
    client = MongoClient(uri)
    db = client['myDatabase']
    user_collection = db['users']

    credentials = load_credentials()
    username = next(iter(credentials))

    # Find the user by username
    user = user_collection.find_one({'username': username})
    if not user:
        print("Please login first.")
    else:
        if user['username'] in credentials:
            files = user["files"]
            try:
                for file_info in files:
                    if str(file_info['file_name']) == str(file_number_or_cid):
                        file_name = file_info['file_name']
                        save_path = os.path.expanduser(f"~/Downloads/{file_name}") 
                    elif int(file_info['file_number']) == int(file_number_or_cid):
                        file_name = file_info['file_name']
                        save_path = os.path.expanduser(f"~/Downloads/{file_name}") 
            except ValueError as e:
                print("The file is not located in the databse")
                return

            file_path = os.path.expanduser(f"~/BCloud/{file_name}")
            sender_socket = connect_to_relay_server()



             # Send a header with the file name
            file_name = os.path.basename(file_path)
            file_header = f"FILE_REQUEST:{file_name}:"
            sender_socket.send(file_header.encode())
            sender_socket.send(b"END_OF_HEADER") # delimiter to notify the server that the header is done

            end_of_header = b"END_OF_HEADER"
            buffer = b""
            header = None
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
                    file_name = split_header[1]
                    file_size = split_header[2]
                    buffer = content 

                if file_type == "FILE_REQUEST_RESPONSE":
                    # It's a file; process the file header to get file info

                    directory_name = "Downloads"
                    directory_path = os.path.expanduser(f"~/{directory_name}")
                    file_save_path = os.path.join(directory_path, file_name)

                    # Check if the directory exists, create if it does not and create a welcome text file
                    if not os.path.exists(directory_path):
                        os.makedirs(directory_path, exist_ok=True)
                        welcome_file_path = os.path.join(directory_path, "welcome.txt")
                        with open(welcome_file_path, 'w') as welcome_file:
                            welcome_file.write("Welcome to Banbury Cloud! This is the directory that will contain all of the files "
                                               "that you would like to have in the cloud and streamed throughout all of your devices. "
                                               "You may place as many files in here as you would like, and they will appear on all of "
                                               "your other devices.")

                    # Send acknowledgment (optional)
                    #self.client_socket.send("ACK".encode())
                        # Open the file and start writing the content received so far


                    with open(file_save_path, 'wb') as file:
                        file.write(buffer)  # Write already received part of the file
                        bytes_received = len(buffer)  # Update the count of received bytes
                        # Continue receiving the rest of the file
                        while bytes_received < int(file_size):
                            data = sender_socket.recv(4096)
                            if not data:
                                break  # Connection is closed or error occurred
                            file.write(data)
                            bytes_received += len(data)

                    job_completed = True 



                    print(f"File downloaded and saved as {file_save_path}")
                else:
                    print("No username found. Please register or login.")


def summary():
    load_dotenv()
    uri = os.getenv("MONGODB_URL")
 
    client = MongoClient(uri)
    credentials = load_credentials()
    username = next(iter(credentials))
    db = client['myDatabase']
    user_collection = db['users']
    user = user_collection.find_one({'username': username})
    if not user:
        print("Please login first.")
    else:
        if user['username'] in credentials:
            try:
                devices = user.get('devices', [])
                num_devices = len(devices)
                total_storage_capacity = sum(device.get('storage_capacity_GB', 0) for device in devices)  # Calculate total storage capacity
                files = user.get('files', [])
                num_files = len(files)
                summary = [["Number of Devices", num_devices],["Total Storage Capacity (GB)", total_storage_capacity],["Number of Files", num_files]]
                print(tabulate(summary, tablefmt='rounded_grid'))
            except Exception as e:
                print(f"Error displaying files: {e}")
        else:
            print("No username found. Please register or login.")

def upload_file(file_path):
    try:

        file_name = file_path.split('/')[-1]
        file_destination_path = os.path.expanduser(f"~/BCloud/{file_name}")
        # Check if file already exists at destination path
        if os.path.isfile(file_destination_path):
            print(f"File already exists at {file_destination_path}")
        else:
            # Copy the file from source to destination
            shutil.copy2(file_path, file_destination_path)

        # Upload the actual file
        file_size_result = subprocess.run(["du", "-h", file_path], capture_output=True, text=True, check=True)
        file_size = file_size_result.stdout.strip().split()[-2]

        command = "hostname"
        device_name_result = subprocess.run(command, shell=True, check=True, text=True, stdout=subprocess.PIPE)
        device_name = device_name_result.stdout.strip()  # Remove leading/trailing whitespace

        # Add the data to the database
        load_dotenv()
        uri = os.getenv("MONGODB_URL")
 
        client = MongoClient(uri)
        db = client['myDatabase']
        user_collection = db['users']
        credentials = load_credentials()
        username = next(iter(credentials))
        user = user_collection.find_one({'username': username})
        if not user:
            print("Please login first.")
        else:
            if user['username'] in credentials:
                current_file_count = len(user.get('files', []))
                file_number = current_file_count + 1
                # Add file information to the MongoDB 'files' array
                file_info = {
                    'file_number' : file_number, 
                    'file_name': file_name,
                    'size': file_size, 
                    'file_location': device_name,
                    'upload_date': datetime.now(),
                }
                user_collection.update_one({'_id': user['_id']}, {'$push': {'files': file_info}})
                print(f"File uploaded and saved to cloud")
            else:
                print("No username found. Please register or login.")
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")



def delete_file(file_number_or_cid):
    try:
        # Connect to MongoDB
        load_dotenv()
        uri = os.getenv("MONGODB_URL")
 
        client = MongoClient(uri)
        db = client['myDatabase']
        user_collection = db['users']

        credentials = load_credentials()
        username = next(iter(credentials))
        user = user_collection.find_one({'username': username})

        if not user:
            print("Please login first.")
        else:
            if user['username'] in credentials:
                files = user.get('files', [])
                found = False  # Flag to track if the file was found

                # Create a new list of files excluding the one to be deleted
                updated_files = [file for file in files if file['cid'] != file_number_or_cid and str(file['file_number']) != str(file_number_or_cid)]

                if len(updated_files) < len(files):
                    # Update the 'files' array with the filtered list
                    user_collection.update_one({'_id': user['_id']}, {'$set': {'files': updated_files}})
                    print(f"File(s) with file number or CID {file_number_or_cid} have been deleted")
                else:
                    print(f"No files matching {file_number_or_cid} found.")
            else:
                print("No username found. Please register or login.")
    except Exception as e:
        print(f"Error: {e}")

def list_devices():
    credentials = load_credentials()
    load_dotenv()
    uri = os.getenv("MONGODB_URL")
 
    client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
    username = next(iter(credentials))    
    db = client['myDatabase']
    user_collection = db['users']
    user = user_collection.find_one({'username': username})
    if not user:
        print("Please login first.")
    else:
        if user['username'] in credentials:
            try:
                devices = user['devices']
                if devices:
                    columns_to_exclude = ['network_speeds', 'network_reliability','average_time_online','sync_status','optimization_status','device_priority']
                    headers = [key for key in devices[0].keys() if key not in columns_to_exclude]
                    #headers = [key for key in devices[0].keys() if key != 'network_speeds']  # Exclude 'network_speeds' from headers
                    rows = [[item[key] for key in headers] for item in devices]

                    print(tabulate(rows, headers=headers, tablefmt='rounded_grid'))
                else:
                    print("No devices found for this user")
            except Exception as e:
                print(f"Error displaying files:L {e}")
        else:
            print("No username found. Please register or login.")



def add_device():
    try:
        load_dotenv()
        uri = os.getenv("MONGODB_URL")
 
        client = MongoClient(uri)
        db = client['myDatabase']
        user_collection = db['users']
        
        credentials = load_credentials()
        username = next(iter(credentials))
        
        user = user_collection.find_one({'username': username})

        if not user:
            print("Please login first.")
        else:
            if user['username'] in credentials:

                command = "speedtest"
                network_speed_result = subprocess.run(command, shell=True, capture_output=True, check=True, text=True)
                # Use regular expressions to extract the Wi-Fi speed
                download_speed_pattern = r"Download:\s+(\d+(\.\d+)?)\s[MG]?bit/s"
                match = re.search(download_speed_pattern, network_speed_result.stdout)
                if match:
                    download_speed_value = match.group(1)
                    download_network_speed = download_speed_value
                else:
                    download_network_speed = 0

                upload_speed_pattern = r"Upload:\s+(\d+(\.\d+)?)\s[MG]?bit/s"
                match = re.search(upload_speed_pattern, network_speed_result.stdout)
                if match:
                    upload_speed_value = match.group(1)
                    upload_network_speed = upload_speed_value
                else:
                    upload_network_speed = 0

                time = datetime.now()
                network_speeds = {
                        'download_network_speed': download_network_speed,    
                        'upload_network_speed': upload_network_speed, 
                        'time': time
                } 

                command = "hostname"
                device_name_result = subprocess.run(command, shell=True, check=True, text=True, stdout=subprocess.PIPE)
                device_name = device_name_result.stdout.strip()  # Remove leading/trailing whitespace

                command = "df -h"
                device_capacity_result = subprocess.run(command, shell=True, check=True, text=True, stdout=subprocess.PIPE)
                device_capacity_output = device_capacity_result.stdout.strip()  # Capture the output
                

                # Split the output into lines
                output_lines = device_capacity_output.split('\n')

                # Extract the sizes from the output and calculate the total capacity
                total_capacity = 0  # Initialize total capacity as 0
                for line in output_lines[1:]:  # Skip the header line
                    columns = line.split()
                    if len(columns) >= 2:
                        size_str = columns[1]
                        # Remove non-numeric characters and convert to bytes
                        if size_str.endswith('G'):
                            size = float(size_str.rstrip('G')) * 1e9  # Convert gigabytes to bytes
                        elif size_str.endswith('T'):
                            size = float(size_str.rstrip('T')) * 1e12  # Convert terabytes to bytes
                        elif size_str.endswith('M'):
                            size = float(size_str.rstrip('M')) * 1e6  # Convert megabytes to bytes
                        elif size_str.endswith('K'):
                            size = float(size_str.rstrip('K')) * 1e3  # Convert kilobytes to bytes
                        else:
                            size = 0  # No suffix, assume bytes
                        total_capacity += size
                storage_capacity = total_capacity / 1e9  # Convert to gigabytes (GB)

                current_device_count = len(user.get('devices', []))
                device_number = current_device_count + 1
                network_speeds = []  
                
                response = requests.get('https://httpbin.org/ip')
                ip_address = response.json()
                origin = ip_address.get('origin', 'Unknown')
                ip_address = origin.split(',')[0]

                # Add device information to the MongoDB 'devices' array
                device_info = {
                    'device_number': device_number,
                    'device_name': device_name,
                    'storage_capacity_GB': storage_capacity,
                    'date_added': datetime.now(),
                    'ip_address': ip_address,
                    'average_network_speed': download_network_speed,  # Initial value
                    'network_speeds': network_speeds,  # Initial value
                    'network_reliability': 0,  # Initial value
                    'average_time_online': 0,  # Initial value
                    'device_priority': 1,  # Initial value
                    'sync_status': True,
                    'optimization_status': True
                }
                
                user_collection.update_one({'_id': user['_id']}, {'$push': {'devices': device_info}})
                print(f"Device info saved to cloud")
            else:
                print("No username found. Please register or login.")
    except subprocess.CalledProcessError as e:
        print(f"Error running IPFS command: {e}")
def delete_device(device_number_or_name):
    try:
        # Connect to MongoDB
        load_dotenv()
        uri = os.getenv("MONGODB_URL")
 
        client = MongoClient(uri)
        db = client['myDatabase']
        user_collection = db['users']

        credentials = load_credentials()
        username = next(iter(credentials))
        user = user_collection.find_one({'username': username})

        if not user:
            print("Please login first.")
        else:
            if user['username'] in credentials:
                devices = user.get('devices', [])
                found = False  # Flag to track if the file was found

                # Create a new list of files excluding the one to be deleted
                updated_devices = [device for device in devices if device['device_name'] != device_number_or_name and str(device['device_number']) != str(device_number_or_name)]

                if len(updated_devices) < len(devices):
                    # Update the 'files' array with the filtered list
                    user_collection.update_one({'_id': user['_id']}, {'$set': {'devices': updated_devices}})
                    print(f"File(s) with file number or CID {device_number_or_name} have been deleted")
                else:
                    print(f"No files matching {device_number_or_name} found.")
            else:
                print("No username found. Please register or login.")
    except Exception as e:
        print(f"Error: {e}")

def ping_device(ping_device_number_or_name):
    remote_host = "michael-ubuntu"
    device_username = "mmills"
    password = "dirtballer"

    try:
        # Connect to MongoDB
        load_dotenv()
        uri = os.getenv("MONGODB_URL")
 
        client = MongoClient(uri)
        db = client['myDatabase']
        user_collection = db['users']

        credentials = load_credentials()  # Assuming load_credentials is defined elsewhere
        username = next(iter(credentials))
        user = user_collection.find_one({'username': username})

        if not user:
            print("Please login first.")
        else:
            if user['username'] in credentials:
                devices = user.get('devices', [])

                # Iterate through the devices to find the correct remote_host
                for device in devices:
                    if device['device_name'] == ping_device_number_or_name or str(device['device_number']) == str(ping_device_number_or_name):
                        remote_host = device['device_name']

                        command = "iwconfig"
                        network_speed_result = subprocess.run(command, shell=True, capture_output=True, check=True, text=True)
                        # Use regular expressions to extract the Wi-Fi speed
                        speed_pattern = r"Bit Rate=(\d+(\.\d+)?)\s[MG]?b/s"
                        match = re.search(speed_pattern, network_speed_result.stdout)
                        if match:
                            speed_value = match.group(1)
                            network_speed = speed_value
                        else:
                            network_speed = 0

                        # Append the network speed to the 'network_speeds' array in the device document
                        device['network_speeds'].append(network_speed)
                        # Update the user collection to reflect the changes
                        user_collection.update_one({'_id': user['_id']}, {'$set': {'devices': devices}})



                        print(f"Network Speed for {device['device_name']}: {network_speed}")
    except Exception as e:
        print(f"Error: {e}")
def main():

    parser = argparse.ArgumentParser(description="A simple CLI template in Python")
    
    subparsers = parser.add_subparsers(dest='command')
    subparsers.add_parser("register", help="Register a new user")
    subparsers.add_parser("login", help="Log in with an existing user")
    subparsers.add_parser("files", help="List files")
    subparsers.add_parser("devices", help="List devices")
    subparsers.add_parser("adddevice", help="Add a device")
    download_parser = subparsers.add_parser("download", help="Download a file")
    download_parser.add_argument("file", help="File to download")
    subparsers.add_parser("summary", help="Show summary")
    upload_parser = subparsers.add_parser("upload", help="Upload a file")
    upload_parser.add_argument("file_path", help="Path of file to upload")
    deletefile_parser = subparsers.add_parser("deletefile", help="Delete a file")
    deletefile_parser.add_argument("file_path_delete", help="Path of file to delete")
    deletedevice_parser = subparsers.add_parser("deletedevice", help="Delete a device")
    deletedevice_parser.add_argument("device_number_or_name", help="Number or name of device to delete")
    pingdevice_parser = subparsers.add_parser("pingdevice", help="Ping a device")
    pingdevice_parser.add_argument("ping_device_number_or_name", help="Number or name of device to ping")
    args = parser.parse_args()
    # Your CLI logic goes here
    if args.command == "register":
        register()
    elif args.command == "login":
        login()
    elif args.command == "files":
        list_files()
    elif args.command == "devices":
        list_devices()
    elif args.command == "adddevice":
        add_device()
    elif args.command == "download":
        download_file(args.file)
    elif args.command == "summary":
        summary()
    elif args.command == "upload":
        upload_file(args.file_path)
    elif args.command == "deletefile":
        delete_file(args.file_path_delete)
    elif args.command == "deletedevice":
        delete_device(args.device_number_or_name)
    elif args.command == "pingdevice":
        ping_device(args.ping_device_number_or_name)

    else:
        print("")
        print("Welcome to BCloud CLI Tool")
        print("Version 1.0.1")
        print("")
        print("Global options:")
        print(" register                                  Sign up for an account.")
        print(" login                                     Log in to an already existing account.")
        print(" files                                     Print a list of all files in the cloud.")
        print(" devices                                   Print a list of all devices connected to the cloud.")
        print(" adddevice <device_number> <device_name>   Add a device to the cloud.")
        print(" download                                  Download a file from the cloud. Automatically goes to downloads folder.")
        print(" summary                                   Download a file from the cloud. Automatically goes to downloads folder.")
        print(" upload <file_name>                        Upload a new file from the cloud.")
        print(" pingdevice                                Ping a connected device via ssh and receive various device info.")
        print(" deletefile <file_number> <cid>            Delete a file from the cloud")
        print(" deletedevice <device_number> <device_name>Remove a device from the cloud")
        print("")
if __name__ == "__main__":
    main()
