import socket
import threading
import os
import json
import time
from datetime import datetime
import schedule
# from pymongo.mongo_client import MongoClient
from pymongo import MongoClient
from dotenv import load_dotenv
import pymongo
import bcrypt
# from pymongo.server_api import ServerApi
import hashlib
import dotenv
from .LoginHandler import LoginHandler
from .MessageHandler import MessageHandler
from .FileHandler import FileHandler
from .DeviceHandler import DeviceHandler
from .ProfileHandler import ProfileHandler
from .PingHandler import PingHandler


SERVER_HOST = '0.0.0.0'  # Server host IP address
SERVER_PORT = 443  # Server port

class ClientHandler(threading.Thread):
    client_sockets = []
    client_addresses = []
    device_websockets = {}
    device_username = {}
    def __init__(self, client_socket, client_address):
        super().__init__()
        self.client_socket = client_socket
        self.client_address = client_address
        ClientHandler.client_sockets.append(client_socket)
        ClientHandler.client_addresses.append(client_address)
        self.running = True
    def run(self):
        username = None
        password = None
        file_name = None
        device_name = None
        file_size = None
        end_of_header = b"END_OF_HEADER"
        end_of_json = b"END_OF_JSON"
        found_end_of_json = False
        buffer = b""
        header = None

        file_type = "Unknown"
        self.client_socket.settimeout(45)
        while self.running:
            data = self.client_socket.recv(4096)
            if not data:
                break
            buffer += data
            if end_of_header in buffer and header is None:
                header_part, content = buffer.split(end_of_header, 1)
                header = header_part.decode() 
                split_header = header.split(":")
                file_type = split_header[0]
                file_name = split_header[1]
                device_name = split_header[1]
                file_size = split_header[2]
                password = split_header[2]
                username = split_header[3]
                buffer = content 
            if file_type == "MSG":
                message_handler = MessageHandler(self.client_socket)
                message_handler.process_message_request(buffer, username, password)

            elif file_type == "LOGIN_REQUEST":
                login_handler = LoginHandler(self.client_socket)
                login_handler.process_login_request(buffer, username, password)

            elif file_type == "REGISTRATION_REQUEST":
                registration_handler = RegistrationHandler(self.client_socket)
                registration_handler.process_registration_request(buffer, username, password)

            elif file_type == "FILE":
                file_handler = FileHandler(self.client_socket)
                file_handler.process_file(buffer, username, password, file_name, device_name, file_size)
            elif file_type == "FILE_REQUEST":
                file_handler = FileHandler(self.client_socket)
                file_handler.process_file_request(buffer, username, password, file_name, device_name, file_size)
            elif file_type == "FILE_REQUEST_RESPONSE":
                file_handler = FileHandler(self.client_socket)
                file_handler.process_file_request_response(buffer, username, password, file_name, device_name, file_size)
           
            elif file_type == "DEVICE_DELETE_REQUEST":
                device_handler = DeviceHandler(self.client_socket)
                device_handler.process_delete_device_request(buffer, username, password, file_name, device_name, file_size)

            elif file_type == "FILE_DELETE_REQUEST":
                file_handler = FileHandler(self.client_socket)
                file_handler.process_file_request(buffer, username, password, file_name, device_name, file_size)

            elif file_type == "FILE_DELETE_REQUEST_RESPONSE":
                file_handler = FileHandler(self.client_socket)
                file_handler.process_file_request_response(buffer, username, password, file_name, device_name, file_size)


            elif file_type == "CHANGE_PROFILE_REQUEST":
                profile_handler = ProfileHandler(self.client_socket)
                profile_handler.process_change_profile_request(buffer, username, password, file_name, device_name, file_size)

            elif file_type == "SMALL_PING_REQUEST_RESPONSE":

                date_time = datetime.now()
                print(f"{date_time} Received small ping request response")
                message_content = buffer.decode('utf-8')  # Decoding bytes to a string
                end_of_JSON = "END_OF_JSON"
                limited_message_content = message_content.split(end_of_JSON)[0]
                total_json = ""
                if end_of_JSON not in message_content:
                    total_json += message_content
                else:
                    total_json += limited_message_content

                    ping_handler = PingHandler(self.client_address, self.client_socket, self.client_sockets, self.device_username)
                    client_socket = ping_handler.process_small_ping_request_response(total_json, username, password, file_name, device_name, file_size)
                    if client_socket == "device_not_found":
                        print("Device not found, sending ping request")
                        send_ping_no_loop()
                    else:
                        ClientHandler.device_websockets[device_name] = client_socket
                    header = None
                    buffer = b""
                    file_type = "Unknown"


            elif file_type == "PING_REQUEST_RESPONSE":

                date_time = datetime.now()
                print(f"{date_time} Received ping request response")
                message_content = buffer.decode('utf-8')
                end_of_JSON = "END_OF_JSON"
                limited_message_content = message_content.split(end_of_JSON)[0]
                # if end_ofJSON is not in message content,  then the message is incomplete
                total_json = ""
                if end_of_JSON not in message_content:
                    # add meesage_content to a variable called total_json
                    total_json += message_content
                else:
                    # add message_content to a variable called total_json
                    total_json += limited_message_content
                    # parse the JSON

                    ping_handler = PingHandler(self.client_address, self.client_socket, self.client_sockets, self.device_username)
                    ping_handler.process_ping_request_response(total_json, username, password, file_name, device_name, file_size)
                    header = None
                    buffer = b""
                    file_type = "Unknown"


            else:
                print(f"Unknown data type received from {self.client_address}")



                # except Exception as e:
                #     print(f"we are handling a socket timeout {e}")
                #     load_dotenv()
                #     uri = os.getenv("MONGODB_URL")
                #     client = MongoClient(uri)
                #     db = client['myDatabase']
                #     user_collection = db['users']
                #     for client_socket in list(ClientHandler.device_websockets.values()):
                #         if client_socket == self.client_socket:
                #             device_name = reverse_lookup(ClientHandler.device_websockets, client_socket)
                #             username = reverse_lookup(ClientHandler.device_username, client_socket)
                #             # if the username returns none, try another function 
                #             if username == None:
                #                 username = reverse_lookup_list(ClientHandler.device_username, client_socket)
                #             if username and device_name:
                #                 user = user_collection.find_one({'username': username})
                #                 if user:
                #                     devices = user.get('devices', [])
                #                     for device in devices:
                #                         if device.get('device_name') == device_name:
                #                             device['online'] = False
                #                             # break
                #                     user_collection.update_one({'_id': user['_id']}, {'$set': {'devices': devices}})
                #                     print(f"Set {device_name} of {username} to offline")
                #             # Remove the socket from the mappings
                #             ClientHandler.device_websockets.pop(device_name, None)
                #             ClientHandler.device_username.pop(username, None)
                #             # ClientHandler.client_addresses.remove(client_socket) 
                #             ClientHandler.client_sockets.remove(client_socket)
                #         date_time = datetime.now()


        # except Exception as e:
        #     print(f"Ping request failed {e}")
        #     header = None
        #     buffer = b""


def send_small_ping():
        time.sleep(10)

        date_time = datetime.now()
        print(f"{date_time} Sending small ping to all devices")
        while True:
            for client_sock in ClientHandler.client_sockets:
                    perm_sock = client_sock
                    date_time = datetime.now()
                    # print(f"{date_time} Sending ping request to {client_sock}")
                    # print(f"{date_time} Sending small ping request")
                    try:
                        null_string = ""
                        file_header = f"SMALL_PING_REQUEST:{null_string}:{null_string}:END_OF_HEADER"
                        client_sock.send(file_header.encode())
                        #socket.send(b"END_OF_HEADER") # delimiter to notify the server that the header is done

                    except BrokenPipeError:
                        print("Broken pipe, removing socket, setting device to offline, moving on to the next socket.")
                        load_dotenv()
                        uri = os.getenv("MONGODB_URL")
                        client = MongoClient(uri)
                        db = client['myDatabase']
                        user_collection = db['users']
                        # print(ClientHandler.device_websockets)
                        # print(ClientHandler.device_username)
                        device_name = reverse_lookup(ClientHandler.device_websockets, perm_sock)
                        # print(f"Device name: {device_name}")
                        username = reverse_lookup(ClientHandler.device_username, perm_sock)
                        # print(f"Username: {username}")
                        if username == None:
                            print("username is none trying another function")
                            username = reverse_lookup_list(ClientHandler.device_username, perm_sock)
                        if username and device_name:
                            print("passed first if")
                            user = user_collection.find_one({'username': username})
                            if user:
                                print("passed second if")
                                devices = user.get('devices', [])
                                for device in devices:
                                    print("passed third if")
                                    if device.get('device_name') == device_name:
                                        print("passed fourth if")
                                        device['online'] = False
                                        # break
                                user_collection.update_one({'_id': user['_id']}, {'$set': {'devices': devices}})
                                print(f"Set {device_name} of {username} to offline")
                        elif device_name:
                            print("only have device name, looking up user")

                        # Remove the socket from the mappings
                        ClientHandler.device_websockets.pop(device_name, None)
                        ClientHandler.device_username.pop(username, None)
                        # ClientHandler.client_addresses.remove(client_socket) 
                        ClientHandler.client_sockets.remove(client_sock)
                
            time.sleep(10)


def send_ping_no_loop():
        print("sending ping no loop")
        date_time = datetime.now()
        print(f"{date_time} Pinging all devices")
        for client_sock in ClientHandler.client_sockets:
                perm_sock = client_sock
                date_time = datetime.now()
                # print(f"{date_time} Sending ping request to {client_sock}")
                print(f"{date_time} Sending ping request")
                try:
                    null_string = ""
                    file_header = f"PING_REQUEST:{null_string}:{null_string}:END_OF_HEADER"
                    client_sock.send(file_header.encode())
                    #socket.send(b"END_OF_HEADER") # delimiter to notify the server that the header is done

                except BrokenPipeError:
                    print("Broken pipe, removing socket, setting device to offline, moving on to the next socket.")
                    load_dotenv()
                    uri = os.getenv("MONGODB_URL")
                    client = MongoClient(uri)
                    db = client['myDatabase']
                    user_collection = db['users']
                    # print(ClientHandler.device_websockets)
                    # print(ClientHandler.device_username)
                    device_name = reverse_lookup(ClientHandler.device_websockets, perm_sock)
                    # print(f"Device name: {device_name}")
                    username = reverse_lookup(ClientHandler.device_username, perm_sock)
                    # print(f"Username: {username}")
                    if username == None:
                        print("username is none trying another function")
                        username = reverse_lookup_list(ClientHandler.device_username, perm_sock)
                    if username and device_name:
                        print("passed first if")
                        user = user_collection.find_one({'username': username})
                        if user:
                            print("passed second if")
                            devices = user.get('devices', [])
                            for device in devices:
                                print("passed third if")
                                if device.get('device_name') == device_name:
                                    print("passed fourth if")
                                    device['online'] = False
                                    # break
                            user_collection.update_one({'_id': user['_id']}, {'$set': {'devices': devices}})
                            print(f"Set {device_name} of {username} to offline")
                    elif device_name:
                        print("only have device name, looking up user")

                    # Remove the socket from the mappings
                    ClientHandler.device_websockets.pop(device_name, None)
                    ClientHandler.device_username.pop(username, None)
                    # ClientHandler.client_addresses.remove(client_socket) 
                    ClientHandler.client_sockets.remove(client_sock)
                # print(f"{date_time} All connected client addresses: {ClientHandler.client_addresses}")
                # print(f"{date_time} All connected client devices: {ClientHandler.device_websockets}")
                # print(f"{date_time} All connected client users: {ClientHandler.device_username}")
            


def send_ping():
        send_small_ping()
        time.sleep(10)
        date_time = datetime.now()
        print(f"{date_time} Pinging all devices")
        while True:
            for client_sock in ClientHandler.client_sockets:
                    perm_sock = client_sock
                    date_time = datetime.now()
                    # print(f"{date_time} Sending ping request to {client_sock}")
                    print(f"{date_time} Sending ping request")
                    try:
                        null_string = ""
                        file_header = f"PING_REQUEST:{null_string}:{null_string}:END_OF_HEADER"
                        client_sock.send(file_header.encode())
                        #socket.send(b"END_OF_HEADER") # delimiter to notify the server that the header is done

                    except BrokenPipeError:
                        print("Broken pipe, removing socket, setting device to offline, moving on to the next socket.")
                        load_dotenv()
                        uri = os.getenv("MONGODB_URL")
                        client = MongoClient(uri)
                        db = client['myDatabase']
                        user_collection = db['users']
                        # print(ClientHandler.device_websockets)
                        # print(ClientHandler.device_username)
                        device_name = reverse_lookup(ClientHandler.device_websockets, perm_sock)
                        # print(f"Device name: {device_name}")
                        username = reverse_lookup(ClientHandler.device_username, perm_sock)
                        # print(f"Username: {username}")
                        if username == None:
                            print("username is none trying another function")
                            username = reverse_lookup_list(ClientHandler.device_username, perm_sock)
                        if username and device_name:
                            print("passed first if")
                            user = user_collection.find_one({'username': username})
                            if user:
                                print("passed second if")
                                devices = user.get('devices', [])
                                for device in devices:
                                    print("passed third if")
                                    if device.get('device_name') == device_name:
                                        print("passed fourth if")
                                        device['online'] = False
                                        # break
                                user_collection.update_one({'_id': user['_id']}, {'$set': {'devices': devices}})
                                print(f"Set {device_name} of {username} to offline")
                        elif device_name:
                            print("only have device name, looking up user")

                        # Remove the socket from the mappings
                        ClientHandler.device_websockets.pop(device_name, None)
                        ClientHandler.device_username.pop(username, None)
                        # ClientHandler.client_addresses.remove(client_socket) 
                        ClientHandler.client_sockets.remove(client_sock)
                    # print(f"{date_time} All connected client addresses: {ClientHandler.client_addresses}")
                    # print(f"{date_time} All connected client devices: {ClientHandler.device_websockets}")
                    # print(f"{date_time} All connected client users: {ClientHandler.device_username}")
                
            time.sleep(10)


            # time.sleep(600)


def reverse_lookup(dictionary, value):
    for key, val in dictionary.items():
        if val == value:
            return key
    return None

def reverse_lookup_list(dictionary, value):
    for key, sockets in dictionary.items():
        if value in sockets:
            return key
    return None


def main():


    print("Welcome to the Banbury Relay Server")


    print("Initializing database...")
    # Iterate through every device of every user, set every device to offline
    load_dotenv()
    uri = os.getenv("MONGODB_URL")
    client = MongoClient(uri)
    db = client['myDatabase']
    user_collection = db['users']
    for user in user_collection.find():
        if user:
            devices = user.get('devices', [])
            for device in devices:
                device['online'] = False
            user_collection.update_one({'_id': user['_id']}, {'$set': {'devices': devices}})


    # Create a server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    # server_socket.settimeout(60)
    date_time = datetime.now()
    print(f"{date_time} Server listening on {SERVER_HOST}:{SERVER_PORT}")
    client_sockets = []
    client_addresses = []
    client_handlers = {}
    running = True
    try:
        # threading.Thread(target=send_ping, daemon=True).start()
        threading.Thread(target=send_ping, daemon=True).start()
        while running:
            # Accept incoming connections
            schedule.run_pending()
            client_socket, client_address = server_socket.accept()

            date_time = datetime.now()
            print(f"{date_time} Accepted connection from {client_address}")
            # Start a new thread to handle the client
            client_handler = ClientHandler(client_socket, client_address)
            client_handler.start()

            unique_identifier = str(client_address)
            client_handlers[unique_identifier] = client_handler
            date_time = datetime.now()
            # print(f"{date_time} All connected client addresses: {ClientHandler.client_addresses}")
            # print(f"{date_time} All connected devices: {ClientHandler.device_websockets}")

    except KeyboardInterrupt:
        print("Server shutting down...")
        running = False
        server_running = False
        for client_socket in ClientHandler.client_sockets:
            client_socket.close()
        server_socket.close()
    finally:
        for client_socket in ClientHandler.client_sockets:
            client_socket.close()
        server_socket.close()
        print("Server has been shut down.")

if __name__ == "__main__":
    main()

