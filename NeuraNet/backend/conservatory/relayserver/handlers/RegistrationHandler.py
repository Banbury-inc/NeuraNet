# login_handler.py

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime
import bcrypt
import json

class RegistrationHandler:
    def __init__(self, client_socket):
        self.client_socket = client_socket

    def process_registration_request(self, buffer, username, password):

        # It's a regular message; process and broadcast it
        message_content = buffer.decode()

        end_of_JSON = "END_OF_JSON"
        limited_message_content = message_content.split(end_of_JSON)[0]
        # if end_ofJSON is not in message content,  then the message is incomplete
        total_json = ""
        if end_of_JSON not in message_content:
            # add meesage_content to a variable called total_json
            total_json += message_content
        elif end_of_JSON in message_content:
            # add message_content to a variable called total_json
            total_json += limited_message_content
            # parse the JSON
            try:
                data = json.loads(total_json)
                
            except json.JSONDecodeError as e:
                print(f"JSON decode error {e}")
                data = None

            username = data["username"]
            password = data["password"]
            firstName = data["first_name"]
            lastName = data["last_name"]

            password_bytes = password.encode('utf-8')  # Encode the string to bytes
            load_dotenv()
            uri = os.getenv("MONGODB_URL")

            client = MongoClient(uri)
            db = client['myDatabase']
            user_collection = db['users']
            hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

            # Check if the username already exists
            existing_user = user_collection.find_one({'username': username})

            # If the username already exists, respond with a registration failure message
            result = ""
            if existing_user:
                result = "user_already_exists" 
            else:
                result = "success"
            # Create a new user document with additional fields set to null
            new_user = {
                "username": username,
                "password": hashed_password,
                "first_name": firstName,
                "last_name": lastName,
                "phone_number": None,
                "email": None,
                "devices": [],
                "number_of_devices": [],
                "number_of_files": [],
                "overall_date_added": [],
                "total_average_download_speed": [],
                "total_average_upload_speed": [],
                "total_device_storage": [],
                "total_average_cpu_usage": [],
                "total_average_gpu_usage": [],
                "total_average_ram_usage": [],
            }

            # check to see if the username already exists

            for socket in ClientHandler.client_sockets:
                if socket == self.client_socket:
                    if result == "success":
                        try:
                            user_collection.insert_one(new_user)
                            file_header = f"REGISTRATION_SUCCESS"
                            socket.send(file_header.encode())
                            socket.send(b"END_OF_HEADER") # delimiter to notify the server that the header is done
                        except Exception as e:
                            print(f"Error sending to device: {e}")

                    if result == "user_already_exists":
                        try:
                            file_header = "REGISTRATION_FAILURE_USER_ALREADY_EXISTS"
                            socket.send(file_header.encode())
                            socket.send(b"END_OF_HEADER") # delimiter to notify the server that the header is done
                        except Exception as e:
                            print(f"Error sending to device: {e}")



