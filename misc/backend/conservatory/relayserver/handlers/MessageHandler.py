# login_handler.py

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime
import bcrypt

class MessageHandler:
    def __init__(self, client_socket):
        self.client_socket = client_socket

    def process_message_request(self, buffer, username, password):
        # It's a regular message; process and broadcast it
        message_content = buffer.decode()

        date_time = datetime.now()
        print(f"{date_time} Received message from {self.client_address}: {message_content}")
        # Broadcast the data to each of the clients in the list of addresses
        for socket in ClientHandler.client_sockets:
            if socket != self.client_socket:
                try:
                    socket.sendall(buffer)
                except Exception as e:
                    print(f"Error sending to client")

