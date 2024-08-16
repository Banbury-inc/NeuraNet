# login_handler.py

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime
import bcrypt

class DeviceHandler:
    def __init__(self, client_socket):
        self.client_socket = client_socket

    def process_delete_device_request(self, buffer, username, password, file_name, device_name, file_size):

        # It's a file; process the file header to get file info

        date_time = datetime.now()
        print(f"{date_time} Received device delete request from {self.client_address}: {self.client_socket}")
        print(f"{date_time} Client is requesting to delete {device_name} from {username}'s devices.")
        # Load Database
        load_dotenv()
        uri = os.getenv("MONGODB_URL")

        client = MongoClient(uri)
        db = client['myDatabase']
        user_collection = db['users']
        user = user_collection.find_one({'username': username})

                   # Find the user document and remove the device with the specified device_name
        result = user_collection.update_one(
            {'username': username},
            {'$pull': {'devices': {'device_name': device_name}}}
        )                

        # Check if the update was successful
        if result.modified_count > 0:
            print("Device successfully deleted.")
        else:
            print("No matching device found or deletion failed.")


