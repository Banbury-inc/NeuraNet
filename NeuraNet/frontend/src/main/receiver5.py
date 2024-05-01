import socket
from dotenv import load_dotenv
import sys
import subprocess
import threading
import os
import json
import re
from datetime import datetime, timedelta
import requests
import configparser
import pymongo
import time
import psutil
import GPUtil

def run(receiver_socket):
    end_of_header = b"END_OF_HEADER"
    buffer = b""
    header = None
    file_type = "Unknown"

    while True:

        sys.stdout.flush()
        data = receiver_socket.recv(4096)
        print(data)
        if not data:
            break
        buffer += data
        if end_of_header in buffer and header is None:
            header_part, content = buffer.split(end_of_header, 1)
            header = header_part.decode() 
            split_header = header.split(":")
            file_type = split_header[0]
            file_name = split_header[1]
            file_size = split_header[2]
            password = split_header[2]
            username = split_header[3]
            buffer = content 

        if file_type == "MSG":
            # It's a regular message; process and broadcast it
            message_content = buffer.decode()
            print(f"Received message: {message_content}")

            sys.stdout.flush()

        elif file_type == "UPDATE":

            date_time = get_current_date_and_time()
            print(f"{date_time} Received an update request")
            print("UPDATE")
            #receiver_socket.send(b"END_OF_HEADER") # delimiter to notify the server that the header is done
            sys.stdout.flush()
            data = None 
            buffer = b""
            header = None
            file_type = ""


        elif file_type == "FILE":
            # It's a file; process the file header to get file info
            # Receive the file info (file name and size)
            print("Receiving file...")


            directory_name = "BCloudReceiver"
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
                    data = receiver_socket.recv(4096)
                    if not data:
                        break  # Connection is closed or error occurred
                    file.write(data)
                    bytes_received += len(data)

            print(f"Received {file_name}.")


        elif file_type == "FILE_REQUEST":
            directory_name = "BCloud"
            directory_path = os.path.expanduser(f"~/{directory_name}")
            file_save_path = os.path.join(directory_path, file_name)
            print(f"Device is requesting file: {file_name}")
            file_name = os.path.basename(file_save_path)
            try:
                # Attempt to open the file
                with open(file_save_path, 'rb') as file:
                    file_size = os.path.getsize(file_save_path)
                    print(f'The file size of {file_name} is {file_size} bytes')
                    print("Sending a file request response")
                    null_string = ""
                    file_header = f"FILE_REQUEST_RESPONSE:{file_name}:{file_size}:{null_string}:END_OF_HEADER"
                    receiver_socket.send(file_header.encode())
                    total_bytes_sent = 0
                    while total_bytes_sent < file_size:
                        print("sending file...")
                        bytes_read = file.read(4096)  # Read the file in chunks
                        receiver_socket.sendall(bytes_read)
                        total_bytes_sent =+ len(bytes_read)
                    print(f"{file_name} has been sent successfully.")
                    data = None 
                    buffer = b""
                    header = None
                    file_type = ""

            except FileNotFoundError:
                # Handle the case where the file doesn't exist
                print(f"Error: File '{file_name}' not found.")
                # Send an appropriate response to the client indicating that the file doesn't exist

        elif file_type == "FILE_REQUEST_RESPONSE":
            print("received File_REQUEST_RESONSE")


        elif file_type == "PING_REQUEST":
            # It's a regular message; process and broadcast it
            date_time = get_current_date_and_time()
            print(f"{date_time} Received a ping request")
            device_info = None
            device_info = get_device_info()
            null_string = ""
            file_header = f"PING_REQUEST_RESPONSE:{null_string}:{null_string}:{null_string}:END_OF_HEADER"
            receiver_socket.send(file_header.encode())
            device_info_with_stop_signal = f"{device_info}END_OF_JSON"
            #receiver_socket.send(b"END_OF_HEADER") # delimiter to notify the server that the header is done
            receiver_socket.send(device_info_with_stop_signal.encode())

            date_time = get_current_date_and_time()
            print(f"{date_time} Ping response has been sent successfully.")
            data = None 
            buffer = b""
            header = None
            file_type = ""

        elif file_type == "SMALL_PING_REQUEST":
            # It's a regular message; process and broadcast it
            date_time = get_current_date_and_time()
            print(f"{date_time} Received a small ping request")
            device_info = None
            device_info = small_get_device_info()
            null_string = ""
            file_header = f"SMALL_PING_REQUEST_RESPONSE:{null_string}:{null_string}:{null_string}:END_OF_HEADER"
            receiver_socket.send(file_header.encode())
            device_info_with_stop_signal = f"{device_info}END_OF_JSON"
            #receiver_socket.send(b"END_OF_HEADER") # delimiter to notify the server that the header is done
            receiver_socket.send(device_info_with_stop_signal.encode())

            date_time = get_current_date_and_time()
            print(f"{date_time} Ping response has been sent successfully.")
            data = None 
            buffer = b""
            header = None
            file_type = ""


        elif file_type == "FILE_DELETE_REQUEST":

            directory_name = "BCloud"
            directory_path = os.path.expanduser(f"~/{directory_name}")
            file_save_path = os.path.join(directory_path, file_name)

            print(f"Device is requesting to delete file: {file_name}")


            try:

                file_name = os.path.basename(file_save_path)
                file_size = os.path.getsize(file_save_path)

                # search file_save_path for the file and delete it
                if os.path.exists(file_save_path):
                    os.remove(file_save_path)
                    print(f"{file_name} has been deleted successfully.")
                else:
                    print(f"{file_name} does not exist. Doesn't matter because it's supposed to be deleted anyway.")

                print("Sending a confirmation of file deleteion response")
                null_string=""
                file_header = f"FILE_DELETE_REQUEST_RESPONSE:{file_name}:{file_size}:{null_string}:END_OF_HEADER"
                receiver_socket.send(file_header.encode())
                #receiver_socket.send(b"END_OF_HEADER") # delimiter to notify the server that the header is done

                print("Confirmation of file deletion has been send successfully")
                data = None 
                buffer = b""
                header = None
                file_type = ""

            except Exception as e:
                print(f"Error deleting file: {e}") 
                data = None 
                buffer = b""
                header = None
                file_type = ""

        else:
            print(f"Unknown data type received")

        sys.stdout.flush()


def send_profile_info(sender_socket, first_name, last_name, username, email, password):
    date_time = get_current_date_and_time()
    profile_info = {
        'first_name': first_name,
        'last_name': last_name,
        'username': username,
        'email': email,
        'password': password,
    }   
    profile_info_json = json.dumps(profile_info, indent=4)





    null_string = ""
    file_header = f"CHANGE_PROFILE_REQUEST:{null_string}:{null_string}:{null_string}:END_OF_HEADER"
    sender_socket.send(file_header.encode())
    profile_info_with_stop_signal = f"{profile_info_json}END_OF_JSON"
    sender_socket.send(profile_info_with_stop_signal.encode())

    date_time = get_current_date_and_time()
    print(f"{date_time} Ping response has been sent successfully.")





def send_device_info(sender_socket):
    date_time = get_current_date_and_time()
    device_info = None
    device_info = get_device_info()
    null_string = ""
    file_header = f"PING_REQUEST_RESPONSE:{null_string}:{null_string}:{null_string}:END_OF_HEADER"
    sender_socket.send(file_header.encode())
    device_info_with_stop_signal = f"{device_info}END_OF_JSON"
    #receiver_socket.send(b"END_OF_HEADER") # delimiter to notify the server that the header is done
    sender_socket.send(device_info_with_stop_signal.encode())

    date_time = get_current_date_and_time()
    print(f"{date_time} Ping response has been sent successfully.")




def small_send_device_info(sender_socket):
    date_time = get_current_date_and_time()
    device_info = None
    device_info = small_get_device_info()
    null_string = ""
    file_header = f"SMALL_PING_REQUEST_RESPONSE:{null_string}:{null_string}:{null_string}:END_OF_HEADER"
    sender_socket.send(file_header.encode())
    device_info_with_stop_signal = f"{device_info}END_OF_JSON"
    #receiver_socket.send(b"END_OF_HEADER") # delimiter to notify the server that the header is done
    sender_socket.send(device_info_with_stop_signal.encode())

    date_time = get_current_date_and_time()
    print(f"{date_time} Ping response has been sent successfully.")




def small_get_device_info():

    device_name = get_device_name()
    date_and_time = str(get_current_date_and_time())
    files = get_directory_info()
    credentials = load_credentials()
    username = next(iter(credentials))
 

    # Add device information to the MongoDB 'devices' array
    device_info = {
        'user': username,
        'device_number': 1,
        'device_name': device_name,
        'files': files,
        'date_added': date_and_time,
    }
    device_info_json = json.dumps(device_info, indent=4)

    return device_info_json



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



    device_name = get_device_name()
    date_and_time = str(get_current_date_and_time())
    storage_capacity = get_storage_capacity()
    try:
        upload_network_speed, download_network_speed = get_wifi_speed()
    except Exception as e:
        print("Failed to retrieve wifi speed. Setting wifi speeds to 1")
        upload_network_speed = 1
        download_network_speed = 1
    ip_address = get_ip_address()
    files = get_directory_info()
    gpu_usage = get_gpu_usage()
    cpu_usage = get_cpu_usage() 
    ram_usage = get_ram_usage()
    credentials = load_credentials()
    username = next(iter(credentials))
 

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
        "gpu_usage": gpu_usage,
        "cpu_usage": cpu_usage,
        "ram_usage": ram_usage,
        'network_reliability': 0,  # Initial value
        'average_time_online': 0,  # Initial value
        'device_priority': 1,  # Initial value
        'sync_status': True,
        'optimization_status': True
    }
    device_info_json = json.dumps(device_info, indent=4)

    return device_info_json

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
    

def get_gpu_usage():
    """
    Returns the GPU usage.

    Note: This is a very vulnerable function that is likely to have a lot of bugs. I have yet to find a universal solution for all devices. 
    It seems like the GPU driver is primarily responsible for returning this value, which means that we will need to implement a bunch of different
    alternatives for all of the different types of GPU's that are out there. 
    """
    try:
        gpus = GPUtil.getGPUs()
        list_gpus = []
        for gpu in gpus:
            gpu_id = gpu.id
            gpu_name = gpu.name
            gpu_load = gpu.load*100
            gpu_free_memory = f"{gpu.memoryFree}MB"
            gpu_used_memory = f"{gpu.memoryUsed}MB"
            gpu_total_memory = f"{gpu.memoryTotal}MB"
            gpu_temperature = f"{gpu.temperature} °C"
            list_gpus.append(f"ID: {gpu_id}, Name: {gpu_name}, Load: {gpu_load}, Free Memory: {gpu_free_memory}, Used Memory: {gpu_used_memory}, Total Memory: {gpu_total_memory}, Temperature: {gpu_temperature}")
            return gpu_load
    except Exception as e:
        gpu_load = 0
        return gpu_load

def get_cpu_usage():
    """
    Returns the CPU usage.
    """
    cpu_usage = psutil.cpu_percent() 
    return cpu_usage

def get_ram_usage():
    """
    Returns the RAM usage.
    """
    ram = psutil.virtual_memory()
    return ram.percent




def get_current_date_and_time():
    '''
    Gets the current date and time 

    Parameters: N/A

    Returns: string: The current date and time 

    '''
    date_time = datetime.now()
    return date_time

def get_ip_address():
    '''
    Gets the device ip address

    Parameters: N/A

    Returns: string: The ip address of the device 

    '''

    global ip_address
    ip_address = None
    if ip_address is None:
        try:
            response = requests.get('https://httpbin.org/ip')
            ip_info = response.json()
            origin = ip_info.get('origin', 'Unknown')
            ip_address = origin.split(',')[0]
        except requests.exceptions.ConnectionError:
            print("Unable to connect to the server.")
            ip_address = 'Unknown'
    return ip_address
#


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
    return upload_network_speed, download_network_speed

def main():
    load_dotenv()
    SERVER_HOST = os.getenv("RELAY_HOST")
    #SERVER_HOST = "0.0.0.0"
    print("Launching Banbury Cloud")

    sys.stdout.flush()
    SERVER_PORT = 443
    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiver_socket.connect((SERVER_HOST, SERVER_PORT))
    client_sockets = []
    client_addresses = []
    run(receiver_socket)
    receiver_socket.close()

if __name__ == "__main__":
    main()
