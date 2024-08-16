import subprocess
import pymongo
from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient
import schedule
from tabulate import tabulate
import json
import socket
import bcrypt
from dotenv import load_dotenv
import hashlib
import time
import os
import requests
import re
import getpass
from datetime import datetime, timedelta
import configparser

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



def save_credentials(credentials):

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    credentials_file = config.get("banbury_cloud", "credentials_file")
    credentials_file_path = os.path.join(BANBURY_FOLDER, credentials_file)
    with open(credentials_file_path, "w") as file:
        json.dump(credentials, file)



def login():
    username = input("Enter a username: ")
    password_str = getpass.getpass("Enter password: ")
    password_bytes = password_str.encode('utf-8')  # Encode the string to bytes
    load_dotenv()
    uri = os.getenv("MONGODB_URL")
 
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

def connect_to_relay_server():
    load_dotenv()
    RELAY_HOST = os.getenv("RELAY_HOST")
    RELAY_PORT = 8002
 

    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sender_socket.connect((RELAY_HOST, RELAY_PORT))
    return sender_socket

def send_message(message, sender_socket):
    sender_socket.send(message.encode())


def send_messages(sender_socket):
    while True:
        message = input("Type your message (or 'quit' to exit): ")
        if message.lower() == 'quit':
            break
        send_message(message, sender_socket)


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



def request_file(file_path, sender_socket):

    '''
    This function takes a specific file path, sends a request to the relay server notifying the relay
    server that it is requesting a file, waiting for a response from the relay server, and then downloads
    the specific file from the relay server
     

     
    
    Parameters: 


    Returns: print statement confirming that the file has been downloaded 

    '''

     # Send a header with the file name
    file_name = os.path.basename(file_path)
    print(f"File Name: {file_name}")
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
            print(f"header: {header}")
            split_header = header.split(":")
            file_type = split_header[0]
            file_name = split_header[1]
            file_size = split_header[2]
            print(f"file type: {file_type}")
            print(f"file size: {file_size}")
            print(f"file name: {file_name}")
            buffer = content 

        if file_type == "FILE_REQUEST_RESPONSE":
            # It's a file; process the file header to get file info

            print("entering the file request response logic")
            directory_name = "BCloudFILEREQUEST"
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

            print("Receiving file...")
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

            print(f"Received {file_name}.")
            job_completed = True 

def send_file(file_path, sender_socket):

    '''
    This function takes a specific file, reads it on the sending side, sending each chunk over the socket, 
    and then reconstructing the file from these chunks on the server side. 

    This function also creates a header that wraps around the actual file to let the relay server know that 
    this is in fact a file that is coming through and not a message
    Parameters: 


    Returns: print statement confirming that all of the information has been sent to the relay server

    '''

    # Ensure the file exists
    if not os.path.exists(file_path):
        print("File does not exist.")
        return

    # Send a header with the file name and file size
    file_name = os.path.basename(file_path)
    print(f"File Name: {file_name}")
    file_size = os.path.getsize(file_path)
    print(f"File Size: {file_size}")
    file_header = f"FILE:{file_name}:{file_size}:"
    sender_socket.send(file_header.encode())
    sender_socket.send(b"END_OF_HEADER") # delimiter to notify the server that the header is done

    # Wait for server acknowledgment (optional, for synchronization)
    #sender_socket.recv(1024)  # Assuming acknowledgment is within 1024 bytes

    # Send the file in chunks
    with open(file_path, 'rb') as file:
        while True:
            bytes_read = file.read(4096)  # Read the file in chunks
            if not bytes_read:
                break  # File transmission is done
            sender_socket.sendall(bytes_read)

    print(f"{file_name} has been sent successfully.")


def get_device_info():
    '''
    Sends the device info to the relay server in the form of JSON
    - Device Name
    - Current Date and Time
    - Total Number of Files
    - Storage Capacity
    - Current Wifi Speed
    - IP Address
    - Files
        - File Name
        - Date Uploaded
        - File Size
    Parameters: Device name, current_date_and_time, total_number_of_files, storage_capacity, current_wifi_speed, ip_address, files

    Returns: print statement confirming that all of the information has been sent to the relay server

    '''

    credentials = load_credentials()
    username = next(iter(credentials))

    device_name = get_device_name()
    date_and_time = str(get_current_date_and_time())
    storage_capacity = get_storage_capacity()
    upload_network_speed, download_network_speed = get_wifi_speed()
    ip_address = get_ip_address()
    files = get_directory_info()

    # Add device information to the MongoDB 'devices' array
    device_info = {
        'user': username,
        'device_number': 1,
        'device_name': device_name,
        'files': files,
        'storage_capacity_GB': storage_capacity,
        'date_added': date_and_time,
        'ip_address': ip_address,
        'average_network_speed': 0,  # Initial value
        'upload_network_speed': upload_network_speed,  # Initial value
        'download_network_speed': download_network_speed,  # Initial value
        'network_reliability': 0,  # Initial value
        'average_time_online': 0,  # Initial value
        'device_priority': 1,  # Initial value
        'sync_status': True,
        'optimization_status': True
    }
    device_info_json = json.dumps(device_info, indent=4)
    return device_info_json

def get_device_name():
    '''
    Gets the device name

    Parameters: N/A

    Returns: string: The name of the device 

    '''
    command = "hostname"
    device_name_result = subprocess.run(command, shell=True, check=True, text=True, stdout=subprocess.PIPE)
    device_name = device_name_result.stdout.strip()  # Remove leading/trailing whitespace
    return device_name

def get_storage_capacity():
    '''
    Gets the storage capacity

    Parameters: N/A

    Returns: int: The storage capacity of the device in GB 

    '''

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
    return storage_capacity
    


def get_ip_address():
    '''
    Gets the device ip address

    Parameters: N/A

    Returns: string: The ip address of the device 

    '''
    response = requests.get('https://httpbin.org/ip')
    ip_address = response.json()
    origin = ip_address.get('origin', 'Unknown')
    ip_address = origin.split(',')[0]
    return ip_address

def get_wifi_speed():
    '''
    Gets the current device wifi speed. Calculates both the download and upload speeds. 
    Requires speedtest-cli module through linux.

    sudo apt install speedtest-cli

    Also requires the re python module

    Parameters: N/A

    Returns: int: download_network_speed, upload_network_speed 

    '''
    try:
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
    except Exception as e:
        upload_network_speed = 0
        download_network_speed = 0
    return upload_network_speed, download_network_speed

def get_cpu_usage():
    '''
    Gets the current device cpu usage

    Parameters: N/A

    Returns: int: The current cpu usage of the device 

    '''
    pass
def get_gpu_usage():
    '''
    Gets the current device gpu usage

    Parameters: N/A

    Returns: int: The gpu usage of the device 

    '''
    pass
def get_memory_usage():
    '''
    Gets the current device memory usage 

    Parameters: N/A

    Returns: string: The current memory usage of the device 

    '''
    pass
def get_current_date_and_time():
    '''
    Gets the current date and time 

    Parameters: N/A

    Returns: string: The current date and time 

    '''
    date_time = datetime.now()
    return date_time

def get_directory_info():
    '''
    Scans a specific directory and returns all of the information within the directory in the form of JSON 
    - File Name
    - Date Uploaded
    - File Size

    If the directory does not exist, it is created. If it is created, a txt file is created that welcomes the 
    user to banbury cloud

    Parameters: N/A

    Returns: JSON: File name, date uploaded, file size 

    '''
    directory_name = "BCloud"
    directory_path = os.path.expanduser(f"~/{directory_name}")

    # Check if the directory exists, create if it does not and create a welcome text file
    if not os.path.exists(directory_path):
        os.makedirs(directory_path, exist_ok=True)
        welcome_file_path = os.path.join(directory_path, "welcome.txt")
        with open(welcome_file_path, 'w') as welcome_file:
            welcome_file.write("Welcome to Banbury Cloud! This is the directory that will contain all of the files "
                               "that you would like to have in the cloud and streamed throughout all of your devices. "
                               "You may place as many files in here as you would like, and they will appear on all of "
                               "your other devices.")


    # Initialize a list to hold information about each file
    files_info = []

    # Loop through each file in the directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        
        # Skip directories, only process files
        if os.path.isfile(file_path):
            # Get file stats
            stats = os.stat(file_path)
            file_info = {
                "File Name": filename,
                "Date Uploaded": datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                "File Size": stats.st_size
            }
            files_info.append(file_info)

    # Convert the list of dictionaries to JSON format
    return files_info

def send_device_info(): 

    sender_socket = connect_to_relay_server()
    device_info = None
    device_info = get_device_info()
    print("Sending a ping response")
    null_string = ""
    file_header = f"PING_REQUEST_RESPONSE:{null_string}:END_OF_HEADER"
    sender_socket.send(file_header.encode())
    device_info_with_stop_signal = f"{device_info}END_OF_JSON"
    #receiver_socket.send(b"END_OF_HEADER") # delimiter to notify the server that the header is done
    sender_socket.send(device_info_with_stop_signal.encode())



def scheduler():
    '''
    Creates a schedule for when the device will make a ping to the relay server. This will call the function get_device_info which 
    gathers all of the device data and collects it into a json format. 

    the function will print when the last ping was and when the next ping is scheduled

    the scheduler will primarily be set to occur every 30 minutes

    uses the schedule python module
    Parameters: N/A

    Returns: JSON: device_info

    '''
    send_device_info()
    schedule.every(1).minutes.do(send_device_info)

    while True:
        schedule.run_pending()
        time.sleep(1)

def main():
    print("Welcome to Banbury Cloud")
    while True:
        print("1 - Send file")
        print("2 - Request a file")
        print("3 - Send a ping")
        print("4 - Schedule automatic pings")
        command = str(input("What would you like to do? --> "))

        if command == '1':
            print("Beginning send file script...")
            print("Beginning Server Connection...")
            file_path = os.path.expanduser(f"~/BCloud/hiroshi.png")
            sender_socket = connect_to_relay_server()
            send_file(file_path, sender_socket)
        elif command == '2':
            print("Beginning request file script...")
            print("Beginning Server Connection...")
            file_path = os.path.expanduser(f"~/BCloud/hiroshi.png")
            sender_socket = connect_to_relay_server()
            request_file(file_path, sender_socket)
        elif command == '3':
            print("Sending a ping...")

            send_device_info()
        elif command == '4':
            print("Beginning Scheduled Ping Service...")
            scheduler()
        elif command == '5':

            sender_socket = connect_to_relay_server()
            send_messages(sender_socket)

if __name__ == "__main__":
    main()
