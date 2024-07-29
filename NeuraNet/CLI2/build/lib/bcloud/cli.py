import os
import requests
import socket
import re
import argparse
import getpass
import hashlib
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
    uri = "mongodb+srv://mmills6060:Dirtballer6060@banbury.fx0xcqk.mongodb.net/?retryWrites=true&w=majority"
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
    uri = "mongodb+srv://mmills6060:Dirtballer6060@banbury.fx0xcqk.mongodb.net/?retryWrites=true&w=majority"
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
    uri = "mongodb+srv://mmills6060:Dirtballer6060@banbury.fx0xcqk.mongodb.net/?retryWrites=true&w=majority"
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
    try:
        # Search for the file with the given file number in MongoDB
        uri = "mongodb+srv://mmills6060:Dirtballer6060@banbury.fx0xcqk.mongodb.net/?retryWrites=true&w=majority"
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
                for file_info in files:
                    if str(file_info['cid']) == str(file_number_or_cid):
                        cid = file_info['cid']
                        file_name = file_info['file_name']
                        save_path = os.path.expanduser(f"~/Downloads/{file_name}") 
                    if str(file_info['file_name']) == str(file_number_or_cid):
                        cid = file_info['cid']
                        file_name = file_info['file_name']
                        save_path = os.path.expanduser(f"~/Downloads/{file_name}") 
                    if int(file_info['file_number']) == int(file_number_or_cid):
                        cid = file_info['cid']
                        file_name = file_info['file_name']
                        save_path = os.path.expanduser(f"~/Downloads/{file_name}") 

                # Attempt to download the file using the retrieved CID
                command = f"ipfs cat /ipfs/{cid} > {save_path}"
                response = subprocess.run(command, shell=True, check=True, capture_output=True)

                command = f"ipfs pin add {cid}"
                response = subprocess.run(command, shell=True, check=True, capture_output=True)
                if response == "Error: merkledag: not found": 
                    print("Please make sure your daemon is running")
                print(f"File downloaded and saved as {save_path}")
            else:
                print("No username found. Please register or login.")

    except subprocess.CalledProcessError as e:
        error_message = e.stderr.decode('utf-8') if e.stderr else ''
        print(f"Error running IPFS command: {error_message}. Try running daemon first")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def summary():
    uri = "mongodb+srv://mmills6060:Dirtballer6060@banbury.fx0xcqk.mongodb.net/?retryWrites=true&w=majority"
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
        ipfs_result = subprocess.run(["ipfs", "add", file_path], capture_output=True, text=True, check=True)
        ipfs_hash = ipfs_result.stdout.strip().split()[-2]
        file_size_result = subprocess.run(["du", "-h", file_path], capture_output=True, text=True, check=True)
        file_size = file_size_result.stdout.strip().split()[-2]
        print(f"File uploaded to IPFS with hash: {ipfs_hash}")
        uri = "mongodb+srv://mmills6060:Dirtballer6060@banbury.fx0xcqk.mongodb.net/?retryWrites=true&w=majority"
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
                    'file_name': file_path.split('/')[-1],
                    'size': file_size, 
                    'upload_date': datetime.now(),
                    'cid': ipfs_hash
                }
                user_collection.update_one({'_id': user['_id']}, {'$push': {'files': file_info}})
                print(f"File uploaded and saved to cloud")
            else:
                print("No username found. Please register or login.")
    except subprocess.CalledProcessError as e:
        print(f"Error running IPFS command: {e}")



def delete_file(file_number_or_cid):
    try:
        # Connect to MongoDB
        uri = "mongodb+srv://mmills6060:Dirtballer6060@banbury.fx0xcqk.mongodb.net/?retryWrites=true&w=majority"
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
    uri = "mongodb+srv://mmills6060:Dirtballer6060@banbury.fx0xcqk.mongodb.net/?retryWrites=true&w=majority"
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
        uri = "mongodb+srv://mmills6060:Dirtballer6060@banbury.fx0xcqk.mongodb.net/?retryWrites=true&w=majority"
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
        uri = "mongodb+srv://mmills6060:Dirtballer6060@banbury.fx0xcqk.mongodb.net/?retryWrites=true&w=majority"
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
        uri = "mongodb+srv://mmills6060:Dirtballer6060@banbury.fx0xcqk.mongodb.net/?retryWrites=true&w=majority"
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

                        # Create an SSH client
                        ssh_client = paramiko.SSHClient()
                        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                        try:
                            # Connect to the remote host
                            ssh_client.connect(remote_host, username=device_username, password=password)

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
                            print(f"Error: {str(e)}")
                        finally:
                            ssh_client.close()
            else:
                print("No username found. Please register or login.")
    except Exception as e:
        print(f"Error: {e}")
def main():

    parser = argparse.ArgumentParser(description="A simple CLI template in Python")
    
    # Add command-line arguments/options here
    parser.add_argument("--register", action="store_true", help="Register a new user")
    parser.add_argument("--login", action="store_true", help="Log in with an existing user")
    parser.add_argument("--files", action="store_true", help="Log in with an existing user")
    parser.add_argument("--devices", action="store_true", help="Log in with an existing user")
    parser.add_argument("--adddevice", action="store_true", help="Log in with an existing user")
    parser.add_argument("--download", action="store", help="Log in with an existing user")
    parser.add_argument("--summary", action="store_true", help="Log in with an existing user")
    parser.add_argument("--upload", action="store", help="Log in with an existing user")
    parser.add_argument("--pingdevice", action="store", help="Log in with an existing user")
    parser.add_argument("--deletefile", action="store", help="Log in with an existing user")
    parser.add_argument("--deletedevice", action="store", help="Log in with an existing user")
    parser.add_argument("--option1", help="Description for option 1")
    
    args = parser.parse_args()
    
    # Access and use the command-line arguments
    option1_value = args.option1
    option1_value = args.option1
    cid = args.download
    file_path = args.upload
    file_path_delete = args.deletefile
    device_number_or_name = args.deletedevice
    ping_device_number_or_name = args.pingdevice
    
    # Your CLI logic goes here
    if option1_value:
        print(f"Option 1: {option1_value}")
    if args.register:
        register()
    elif args.login:
        login()
    elif args.files:
        list_files()
    elif cid:
        download_file(cid) 
    elif args.summary:
        summary() 
    elif file_path:
        upload_file(file_path)
    elif file_path_delete:
        delete_file(file_path_delete)
    elif args.devices:
        list_devices()
    elif args.adddevice:
        add_device()
    elif device_number_or_name:
        delete_device(device_number_or_name)
    elif ping_device_number_or_name:
        ping_device(ping_device_number_or_name)
 
    else:
        print("Commands:")
        print(" --register                                  Sign up for an account.")
        print(" --login                                     Log in to an already existing account.")
        print(" --files                                     Print a list of all files in the cloud.")
        print(" --devices                                   Print a list of all devices connected to the cloud.")
        print(" --adddevice <device_number> <device_name>   Add a device to the cloud.")
        print(" --download                                  Download a file from the cloud. Automatically goes to downloads folder.")
        print(" --summary                                   Download a file from the cloud. Automatically goes to downloads folder.")
        print(" --upload <file_name>                        Upload a new file from the cloud.")
        print(" --pingdevice                                Ping a connected device via ssh and receive various device info.")
        print(" --deletefile <file_number> <cid>            Delete a file from the cloud")
        print(" --deletedevice <device_number> <device_name>Remove a device from the cloud")
    
if __name__ == "__main__":
    main()
