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
from handlers.ClientHandler import ClientHandler
from handlers.DatabaseHandler import DatabaseHandler
from utils.Lookup import Lookup

SERVER_HOST = '0.0.0.0'  # Server host IP address
SERVER_PORT = 443  # Server port


def send_small_ping():
        time.sleep(10)

        date_time = datetime.now()
        print(f"{date_time} Pinging all devices")
        while True:
            print(f"{date_time} Sending small ping to all devices")
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
        # send_small_ping()
        threading.Thread(target=send_small_ping, daemon=True).start()
        time.sleep(10)
        date_time = datetime.now()
        print(f"{date_time} Pinging all devices")
        while True:
            print(f"{date_time} Sending ping to all devices")
            for client_sock in ClientHandler.client_sockets:
                    perm_sock = client_sock
                    date_time = datetime.now()
                    # print(f"{date_time} Sending ping request to {client_sock}")
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


    print("Welcome to the Banbury Neuranet")


    print("Initializing database...")

    database = DatabaseHandler()
    database.initialize()

    # Create a server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    # server_socket.settimeout(60)
    date_time = datetime.now()
    print(f"{date_time} Server listening on {SERVER_HOST}:{SERVER_PORT}")
    client_handlers = {}
    running = True
    try:
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

