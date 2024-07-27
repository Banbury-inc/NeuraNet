# login_handler.py

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime
import bcrypt

class LoginHandler:
    def __init__(self, client_socket):
        self.client_socket = client_socket

    def process_login_request(self, buffer, username, password):
        message_content = buffer.decode()

        password_bytes = password.encode('utf-8')  # Encode the string to bytes
        load_dotenv()
        uri = os.getenv("MONGODB_URL")

        client = MongoClient(uri)
        db = client['myDatabase']
        user_collection = db['users']
        user = user_collection.find_one({'username': username})
        if user and bcrypt.checkpw(password_bytes, user['password']):
            date_time = datetime.now()
            print(f"{date_time} Login successful!")

            # Send login success message to client
            file_header = "LOGIN_SUCCESS:"
            self.client_socket.send(file_header.encode())
        else:
            # Send login failure message to client
            file_header = "LOGIN_FAIL:"
            self.client_socket.send(file_header.encode())

