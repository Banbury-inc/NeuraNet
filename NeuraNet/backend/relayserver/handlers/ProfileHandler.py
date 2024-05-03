# login_handler.py

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime
import bcrypt
import json

class ProfileHandler:
    def __init__(self, client_socket):
        self.client_socket = client_socket

    def process_change_profile_request(self, buffer, username, password, file_name, device_name, file_size):
        date_time = datetime.now()
        message_content = buffer.decode()
        end_of_JSON = "END_OF_JSON"
        limited_message_content = message_content.split(end_of_JSON)[0]
        total_json = ""
        if end_of_JSON not in message_content:
            total_json += message_content
        elif end_of_JSON in message_content:
            total_json += limited_message_content
            try:
                data = json.loads(total_json)
            except json.JSONDecodeError as e:
                print(f"JSON decode error {e}")
                data = None

        first_name = data["first_name"]
        last_name = data["last_name"]
        username = data["username"]
        email = data["email"]
        password = data["password"]
        password_bytes = password.encode('utf-8')  # Encode the string to bytes
        hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        
        if password == "undefined":
            ClientHandler.device_websockets[device_name] = self.client_socket

            if username in ClientHandler.device_username:
                if self.client_socket not in ClientHandler.device_username[username]:
                    print("current socket not in list of devices, adding")
                    ClientHandler.device_username[username].append(self.client_socket)
            else:
                ClientHandler.device_username[username] = [self.client_socket]

            load_dotenv()
            uri = os.getenv("MONGODB_URL")

            client = MongoClient(uri)
            db = client['myDatabase']
            user_collection = db['users']
            user = user_collection.find_one({'username': username})

            user_collection.update_one({'_id': user['_id']}, {'$set': {
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
                'email': email,
                }})

            date_time = datetime.now()
            header = None
            buffer = b""
            file_type = "Unknown"

            date_time = datetime.now()
            print(f"{date_time} Updated profile info uploaded to Banbury Cloud") 
        else:
            ClientHandler.device_websockets[device_name] = self.client_socket

            if username in ClientHandler.device_username:
                if self.client_socket not in ClientHandler.device_username[username]:
                    print("current socket not in list of devices, adding")
                    ClientHandler.device_username[username].append(self.client_socket)
            else:
                ClientHandler.device_username[username] = [self.client_socket]

            load_dotenv()
            uri = os.getenv("MONGODB_URL")

            client = MongoClient(uri)
            db = client['myDatabase']
            user_collection = db['users']
            user = user_collection.find_one({'username': username})

            user_collection.update_one({'_id': user['_id']}, {'$set': {
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
                'email': email,
                'password': hashed_password,
                }})

            date_time = datetime.now()
            header = None
            buffer = b""
            file_type = "Unknown"

            date_time = datetime.now()
            print(f"{date_time} Updated profile info uploaded to Banbury Cloud") 


