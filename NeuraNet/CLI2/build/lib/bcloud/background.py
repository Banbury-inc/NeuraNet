import os
import logging
import threading
import time
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
import sched
import time
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



def ping_device():
    ping_device_number_or_name = 1
    remote_host = "michael-ubuntu"
    device_username = "mmills"
    password = "dirtballer"

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
                        # Append the network speed to the 'network_speeds' array in the device document
                        device['network_speeds'].append(network_speeds)
                        # Update the user collection to reflect the changes
                        user_collection.update_one({'_id': user['_id']}, {'$set': {'devices': devices}})

                        print(f"Time of ping: {time}")
                        print(f"Download Speed for {device['device_name']}: {download_network_speed}")
                        print(f"Upload Speed for {device['device_name']}: {upload_network_speed}")
                    except Exception as e:
                        print(f"Error: {str(e)}")
                    finally:
                        ssh_client.close()
        else:
            print("No username found. Please register or login.")


scheduler = sched.scheduler(time.time, time.sleep)
def run_ping_device():
    ping_device()

    scheduler.enter(600, 1, run_ping_device)

def schedule(name):
    logging.info("Thread %s: starting", name)
    # Schedule the initial run
    scheduler.enter(0, 1, run_ping_device)
    # Start the scheduler
    scheduler.run()
def run_ipfs_daemon(name):
    logging.info("Thread %s: starting", name)
    command = "ipfs daemon"
    subprocess.run(command, shell=True, capture_output=True, check=True, text=True)
def hello_world(name): 
    logging.info("Thread %s: starting", name)
def main():

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    x = threading.Thread(target=schedule, args=(1,))
    x.start()
    y = threading.Thread(target=run_ipfs_daemon, args=(2,))
    y.start()
    z = threading.Thread(target=run_ipfs_daemon, args=(3,))
    z.start()




if __name__ == "__main__":
    main()





