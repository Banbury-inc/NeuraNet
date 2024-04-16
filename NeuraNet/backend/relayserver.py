import socket
import threading
import os
from dotenv import load_dotenv
import json
import time
from datetime import datetime
import schedule
# from pymongo.mongo_client import MongoClient
from pymongo import MongoClient
import pymongo
import bcrypt
# from pymongo.server_api import ServerApi
import hashlib


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
        end_of_header = b"END_OF_HEADER"
        buffer = b""
        header = None
        file_type = "Unknown"
        self.client_socket.settimeout(45)
        try:
            while self.running:
                try:
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


                    elif file_type == "LOGIN_REQUEST":
                        # It's a regular message; process and broadcast it
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

                            for socket in ClientHandler.client_sockets:
                                if socket == self.client_socket:
                                    try:

                                        file_header = f"LOGIN_SUCCESS:"
                                        socket.send(file_header.encode())
                                        socket.send(b"END_OF_HEADER") # delimiter to notify the server that the header is done

                                    except Exception as e:
                                        print(f"Error sending to device: {e}")

                        else:
                            print("Login unsuccessful!")
                            for socket in ClientHandler.client_sockets:
                                if socket == self.client_socket:
                                    try:

                                        file_header = f"LOGIN_FAIL:"
                                        socket.send(file_header.encode())
                                        socket.send(b"END_OF_HEADER") # delimiter to notify the server that the header is done

                                    except Exception as e:
                                        print(f"Error sending to device: {e}")

                    elif file_type == "REGISTRATION_REQUEST":
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
                                "first_name": "",
                                "last_name": "",
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






                    elif file_type == "FILE":
                        # It's a file; process the file header to get file info

                        directory_name = "BCloudServer"
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

                        date_time = datetime.now()
                        print(f"{date_time} Receiving file...")
                        # Send acknowledgment (optional)
                        #self.client_socket.send("ACK".encode())
                            # Open the file and start writing the content received so far



                        with open(file_save_path, 'wb') as file:
                            file.write(buffer)  # Write already received part of the file
                            bytes_received = len(buffer)  # Update the count of received bytes
                            # Continue receiving the rest of the file
                            while bytes_received < int(file_size):
                                data = self.client_socket.recv(4096)
                                if not data:
                                    break  # Connection is closed or error occurred
                                file.write(data)
                                bytes_received += len(data)

                        date_time = datetime.now()
                        print(f"{date_time} Received {file_name}.")

                        # Broadcast the data to each of the clients in the list of addresses


                        for socket in ClientHandler.client_sockets:
                            if socket != self.client_socket:
                                try:

                                    file_name = os.path.basename(file_save_path)
                                    file_size = os.path.getsize(file_save_path)
                                    file_header = f"FILE:{file_name}:{file_size}:"
                                    socket.send(file_header.encode())
                                    socket.send(b"END_OF_HEADER") # delimiter to notify the server that the header is done

                                    with open(file_save_path, 'rb') as file:
                                        while True:
                                            bytes_read = file.read(4096)  # Read the file in chunks
                                            if not bytes_read:
                                                break  # File transmission is done
                                            socket.sendall(bytes_read)

                                    date_time = datetime.now()
                                    print(f"{date_time} {file_name} has been sent successfully.")



                                except Exception as e:
                                    print(f"Error sending to device: {e}")


                    elif file_type == "FILE_REQUEST":

                        date_time = datetime.now()
                        print(f"Received file request")
                        directory_name = "BCloud"
                        directory_path = os.path.expanduser(f"~/{directory_name}")
                        file_save_path = os.path.join(directory_path, file_name)

                        load_dotenv()
                        uri = os.getenv("MONGODB_URL")
                        client = MongoClient(uri)
                        db = client['myDatabase']
                        user_collection = db['users']
                        user = user_collection.find_one({'username': username})
                        devices = user.get('devices', [])
                        for device in devices:
                            print("searching device")
                            online_status = device.get('online')
                            print(online_status)
                            if online_status == True:
                                print('device is online')
                                for file in device.get('files', []):
                                    if file.get('File Name') == file_name:
                                        print(f"sending file request to {device.get('device_name')}")

                                        # Retrieve the socket associated with the device from device_websockets
                                        target_socket = ClientHandler.device_websockets.get(device.get('device_name'))  # Corrected from device_name to device.get('device_name')
                                        if target_socket:
                                            try:
                                                null_string = ""
                                                file_header = f"FILE_REQUEST:{file_name}:{null_string}:{null_string}:END_OF_HEADER"
                                                date_time = datetime.now()
                                                print(f"{date_time} Sending response with file to device: {device.get('device_name')}")
                                                target_socket.send(file_header.encode())
                                                print("File request sent successfully.")
                                            except Exception as e:
                                                print(f"Error sending file request to device {device.get('device_name')}: {e}")
                                        else:
                                            print(f"No socket found for device {device.get('device_name')}.")

               
                    elif file_type == "FILE_REQUEST_RESPONSE":
                        # It's a file; process the file header to get file info

                        date_time = datetime.now()
                        print(f"{date_time} Received the request")
                        directory_name = "BCloudServer"
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
                                data = self.client_socket.recv(4096)
                                if not data:
                                    break  # Connection is closed or error occurred
                                file.write(data)
                                bytes_received += len(data)

                        print(f"Received {file_name}.")

                        print("Broadcasting to other devices") 
                        # Broadcast the data to each of the clients in the list of addresses

                        for socket in ClientHandler.client_sockets:
                            if socket != self.client_socket:
                                try:
                                    file_name = os.path.basename(file_save_path)
                                    file_size = os.path.getsize(file_save_path)
                                    file_header = f"FILE_REQUEST_RESPONSE:{file_name}:{file_size}:END_OF_HEADER"
                                    socket.send(file_header.encode())
                                    #socket.send(b"END_OF_HEADER") # delimiter to notify the server that the header is done

                                    with open(file_save_path, 'rb') as file:
                                        while True:
                                            bytes_read = file.read(4096)  # Read the file in chunks
                                            if not bytes_read:
                                                break  # File transmission is done
                                            socket.sendall(bytes_read)

                                    print(f"{file_name} has been sent successfully.")
                                    data = None 
                                    buffer = b""
                                    header = None
                                    file_type = ""

                    
                                except BrokenPipeError:
                                    print(f"Broken pipe moving on to the next socket.")
                                    continue  # This skips the rest of the current iteration and moves to the next socket
                                except Exception as e:
                                    print(f"Error sending to device: {e}")

                    elif file_type == "DEVICE_DELETE_REQUEST":
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


                    elif file_type == "FILE_DELETE_REQUEST":
                        # It's a file; process the file header to get file info

                        date_time = datetime.now()
                        print(f"{date_time} Received file delete request from {self.client_address}: {self.client_socket}")
                        directory_name = "BCloud"
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

                        # Load Database
                        load_dotenv()
                        uri = os.getenv("MONGODB_URL")

                        client = MongoClient(uri)
                        db = client['myDatabase']
                        user_collection = db['users']
                        user = user_collection.find_one({'username': username})

                           
                        for socket in ClientHandler.client_sockets:
                            try:
                                # Search each device object in database for a file object that is equal to file_save_path
                                devices = user.get('devices', [])
                                for device in devices:
                                    device_name = device.get('device_name')
                                    for file in device.get('files', []):
                                        if file.get('File Name') == file_name:
                                            file_header = f"FILE_DELETE_REQUEST:{file_name}:{file_size}:{username}:END_OF_HEADER"
                                            socket.send(file_header.encode())
                                            print(f"{file_name} has been requested to be deleted")
                                            data = None 
                                            buffer = b""
                                            header = None
                                            file_type = ""
                
                            except BrokenPipeError:
                                print(f"Broken pipe moving on to the next socket.")
                                continue  # This skips the rest of the current iteration and moves to the next socket
                            except Exception as e:
                                print(f"Error sending to device: {e}")
                

                          
                        try:
                            # Search each device object in database for a file object that is equal to file_save_path
                            devices = user.get('devices', [])
                            file_removed = False
                            for index, device in enumerate(devices):
                                files_to_remove = [file for file in device.get('files', []) if file.get('File Name') == file_name]
                                for some_file in files_to_remove:

                                    date_time = datetime.now()
                                    print(f"{date_time} File detected in database, deleting...")
                                    if any(file['File Name'] == some_file['File Name'] for file in devices[index]['files']):
                                        devices[index]['files'].remove(some_file)  # Add the file if it doesn't exist
                                        user_collection.update_one({'_id': user['_id']}, {'$set': {'devices': devices}})
                                        file_removed = True

                            if file_removed:

                                date_time = datetime.now()
                                print(f"{date_time} {file_name} has been successfully removed from database")
                                data = None 
                                buffer = b""
                                header = None
                                file_type = ""


                            else:
                                print(f"{file_name} not found in the database")
                                data = None 
                                buffer = b""
                                header = None
                                file_type = ""


                        except BrokenPipeError:
                            print(f"Broken pipe moving on to the next socket.")
                            continue  # This skips the rest of the current iteration and moves to the next socket
                        except Exception as e:
                            print(f"Error removing file from database: {e}")




                    elif file_type == "FILE_DELETE_REQUEST_RESPONSE":

                        date_time = datetime.now()
                        print(f"{date_time} Received file delete request response from {self.client_address}: {self.client_socket}")
                        directory_name = "BCloud"
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

                        # Load Database
                        load_dotenv()
                        uri = os.getenv("MONGODB_URL")

                        client = MongoClient(uri)
                        db = client['myDatabase']
                        user_collection = db['users']
                        user = user_collection.find_one({'username': username})

                           
                        for socket in ClientHandler.client_sockets:
                            if socket != self.client_socket:

                                try:
                                    # Search each device object in database for a file object that is equal to file_save_path
                                    devices = user.get('devices', [])
                                    file_removed = False
                                    for index, device in enumerate(devices):
                                        files_to_remove = [file for file in device.get('files', []) if file.get('File Name') == file_name]
                                        for some_file in files_to_remove:

                                            date_time = datetime.now()
                                            print(f"{date_time} File detected in database, deleting...")
                                            if any(file['File Name'] == some_file['File Name'] for file in devices[index]['files']):
                                                devices[index]['files'].remove(some_file)  # Add the file if it doesn't exist
                                                user_collection.update_one({'_id': user['_id']}, {'$set': {'devices': devices}})
                                                file_removed = True
                                                data = None 
                                                buffer = b""
                                                header = None
                                                file_type = ""


                                except BrokenPipeError:
                                    print(f"Broken pipe, removing socket, moving on to the next socket.")
                                    # remove the current socket from the list of client sockets
                                    ClientHandler.client_sockets.remove(socket)
                                    continue  # This skips the rest of the current iteration and moves to the next socket
                                except Exception as e:
                                    print(f"Error sending to device: {e}")


                    elif file_type == "CHANGE_PROFILE_REQUEST":

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
 
     
                
         
                    elif file_type == "SMALL_PING_REQUEST_RESPONSE":

                        date_time = datetime.now()
                        # print(f"{date_time} Received ping request response")
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
                            # try:
                            username = data["user"]
                            device_number = data["device_number"]
                            device_name = data["device_name"]
                            files = data["files"]
                            date_added = data["date_added"]

                            #stay away from this shit
                            ClientHandler.device_websockets[device_name] = self.client_socket

                            if username in ClientHandler.device_username:
                                # if the device is already appended to the list of devices, do nothing
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

                            devices = user.get('devices', [])

                            device_numbers = [device['device_number'] for device in devices]
                            # Find the maximum device number (start from 0 if no devices)
                            max_device_number = max(device_numbers, default=0)

                            for index, device in enumerate(devices):
                                # Check if the current device number is unique
                                if device_numbers.count(device['device_number']) > 1:
                                    # If not unique, assign a new device number
                                    max_device_number += 1
                                    device['device_number'] = max_device_number
                                    print("changed device number")
                                    # Update the device_numbers list for further checks
                                    device_numbers[index] = max_device_number



                            for index, device in enumerate(devices):
                                if device.get('device_name') == device_name:
                                    try:
                                        online = device.get('online')
                                    except Exception as e:
                                        print("online attribute doesn't exist, skipping")

                                    devices[index]['files'] = files

                                    devices[index]['online'] = True
                                    device_exists = True
                                    break  # Exit loop after updating

                            # Update the user document with the modified 'devices' array
                            user_collection.update_one({'_id': user['_id']}, {'$set': {'devices': devices}})

                            # Iterate through devices to aggregate values
                            date_time = datetime.now()
                            # print(f"{date_time} Data uploaded to Banbury Cloud") 
                            header = None
                            buffer = b""
                            file_type = "Unknown"

                            # except Exception as e:
                                # print(f"Error parsing JSON: {e}")





                    elif file_type == "PING_REQUEST_RESPONSE":

                        date_time = datetime.now()
                        print(f"{date_time} Received ping request response")
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
                            # try:
                            username = data["user"]
                            device_number = data["device_number"]
                            device_name = data["device_name"]
                            files = data["files"]
                            number_of_files = str(len(files))
                            storage_capacity_GB = data["storage_capacity_GB"]
                            date_added = data["date_added"]
                            ip_address = data["ip_address"]
                            average_network_speed = data["average_network_speed"]
                            upload_network_speed = data["upload_network_speed"]
                            download_network_speed = data["download_network_speed"]
                            gpu_usage = data["gpu_usage"]
                            cpu_usage = data["cpu_usage"]
                            ram_usage = data["ram_usage"]
                            network_reliability = data["network_reliability"]
                            average_time_online = data["average_time_online"]
                            device_priority = data["device_priority"]
                            sync_status = data["sync_status"]
                            optimization_status = data["optimization_status"]




                            #stay away from this shit
                            ClientHandler.device_websockets[device_name] = self.client_socket

                            if username in ClientHandler.device_username:
                                # if the device is already appended to the list of devices, do nothing
                                if self.client_socket not in ClientHandler.device_username[username]:
                                    print("current socket not in list of devices, adding")
                                    ClientHandler.device_username[username].append(self.client_socket)
                            else:
                                ClientHandler.device_username[username] = [self.client_socket]

                            # print(f"{date_time} All connected devices: {ClientHandler.device_websockets}")
                            # print(f"{date_time} All connected users: {ClientHandler.device_username}")


                            load_dotenv()
                            uri = os.getenv("MONGODB_URL")
         
                            client = MongoClient(uri)
                            db = client['myDatabase']
                            user_collection = db['users']
                            user = user_collection.find_one({'username': username})

                            # If the device was not able to gather the ip_address, just keep it the way it 
                            # was before
                            if ip_address == "Unknown":
                                '''
                                Todo: create logic that will have the database search for what the device IP was previously,
                                and set the variable to whatever it was during the last ping.
                                '''
                                ip_address = "0.0.0.0"

                            devices = user.get('devices', [])
                            total_upload_speed = 0
                            total_download_speed = 0
                            total_gpu_usage = 0
                            total_cpu_usage = 0
                            total_ram_usage = 0
                            upload_speed_count = 0
                            download_speed_count = 0
                            gpu_usage_count = 0
                            cpu_usage_count = 0
                            ram_usage_count = 0

                            device_numbers = [device['device_number'] for device in devices]
                            # Find the maximum device number (start from 0 if no devices)
                            max_device_number = max(device_numbers, default=0)

                            for index, device in enumerate(devices):
                                # Check if the current device number is unique
                                if device_numbers.count(device['device_number']) > 1:
                                    # If not unique, assign a new device number
                                    max_device_number += 1
                                    device['device_number'] = max_device_number
                                    print("changed device number")
                                    # Update the device_numbers list for further checks
                                    device_numbers[index] = max_device_number



                            for index, device in enumerate(devices):
                                if device.get('device_name') == device_name:
                                    upload_speeds = [float(speed) for speed in device.get('upload_network_speed', []) if isinstance(speed, (int, str, float)) and speed != '']
                                    download_speeds = [float(speed) for speed in device.get('download_network_speed', []) if isinstance(speed, (int, str, float)) and speed != '']
                                    gpu_usages = [float(usage) for usage in device.get('gpu_usage', []) if isinstance(usage, (int, str, float)) and usage != '']
                                    cpu_usages = [float(usage) for usage in device.get('cpu_usage', []) if isinstance(usage, (int, str, float)) and usage != '']
                                    ram_usages = [float(usage) for usage in device.get('ram_usage', []) if isinstance(usage, (int, str, float)) and usage != '']
                                    total_upload_speed = sum(upload_speeds) + float(upload_network_speed)
                                    total_download_speed = sum(download_speeds) + float(download_network_speed)
                                    total_gpu_usage = sum(gpu_usages) + float(gpu_usage)
                                    total_cpu_usage = sum(cpu_usages) + float(cpu_usage)
                                    total_ram_usage = sum(ram_usages) + float(ram_usage)
                                    upload_speed_count = len(upload_speeds) + 1
                                    download_speed_count = len(download_speeds) + 1
                                    gpu_usage_count = len(gpu_usages) + 1
                                    cpu_usage_count = len(cpu_usages) + 1
                                    ram_usage_count = len(ram_usages) + 1
                                    average_upload_speed = total_upload_speed / upload_speed_count if upload_speed_count else 0
                                    average_download_speed = total_download_speed / download_speed_count if download_speed_count else 0
                                    average_gpu_usage = total_gpu_usage / gpu_usage_count if gpu_usage_count else 0
                                    average_cpu_usage = total_cpu_usage / cpu_usage_count if cpu_usage_count else 0
                                    average_ram_usage = total_ram_usage / ram_usage_count if ram_usage_count else 0
                                    try:
                                        online = device.get('online')
                                    except Exception as e:
                                        print("online attribute doesn't exist, skipping")



                                    # Update existing device in the list
                                    devices[index]['upload_network_speed'].append(float(upload_network_speed))
                                    devices[index]['download_network_speed'].append(float(download_network_speed))
                                    devices[index]['date_added'].append(date_added)
                                    devices[index]['gpu_usage'].append(float(gpu_usage))
                                    devices[index]['cpu_usage'].append(float(cpu_usage))
                                    devices[index]['ram_usage'].append(float(ram_usage))


                                    # # Instead of directly appending or extending, check if the file exists
                                    # for new_file in files:  # Iterate through the new files to be added
                                    #     # Check if the file already exists in the 'files' array of the device
                                    #     if not any(file['File Name'] == new_file['File Name'] for file in devices[index]['files']):
                                    #         devices[index]['files'].append(new_file)  # Add the file if it doesn't exist

                                    # # Make a copy of the list to avoid modifying it while iterating
                                    # device_files = devices[index]['files'][:]


                                    devices[index]['files'] = files


                                    devices[index]['average_upload_speed'] = average_upload_speed
                                    devices[index]['average_download_speed'] = average_download_speed
                                    devices[index]['average_gpu_usage'] = average_gpu_usage
                                    devices[index]['average_cpu_usage'] = average_cpu_usage
                                    devices[index]['average_ram_usage'] = average_ram_usage
                                    devices[index]['online'] = True
                                    device_exists = True
                                    break  # Exit loop after updating

                            else:

                                # set up a new device
                                upload_speeds = [float(speed) for speed in device.get('upload_network_speed', []) if isinstance(speed, (int, str, float)) and speed != '']
                                download_speeds = [float(speed) for speed in device.get('download_network_speed', []) if isinstance(speed, (int, str, float)) and speed != '']
                                gpu_usages = [float(usage) for usage in device.get('gpu_usage', []) if isinstance(usage, (int, str, float)) and usage != '']
                                cpu_usages = [float(usage) for usage in device.get('cpu_usage', []) if isinstance(usage, (int, str, float)) and usage != '']
                                ram_usages = [float(usage) for usage in device.get('ram_usage', []) if isinstance(usage, (int, str, float)) and usage != '']
                                total_upload_speed = sum(upload_speeds) + float(upload_network_speed)
                                total_download_speed = sum(download_speeds) + float(download_network_speed)
                                total_gpu_usage = sum(gpu_usages) + float(gpu_usage)
                                total_cpu_usage = sum(cpu_usages) + float(cpu_usage)
                                total_ram_usage = sum(ram_usages) + float(ram_usage)
                                upload_speed_count = len(upload_speeds) + 1
                                download_speed_count = len(download_speeds) + 1
                                gpu_usage_count = len(gpu_usages) + 1
                                cpu_usage_count = len(cpu_usages) + 1
                                ram_usage_count = len(ram_usages) + 1
                                average_upload_speed = total_upload_speed / upload_speed_count if upload_speed_count else 0
                                average_download_speed = total_download_speed / download_speed_count if download_speed_count else 0
                                average_gpu_usage = total_gpu_usage / gpu_usage_count if gpu_usage_count else 0
                                average_cpu_usage = total_cpu_usage / cpu_usage_count if cpu_usage_count else 0
                                average_ram_usage = total_ram_usage / ram_usage_count if ram_usage_count else 0
                                

                                # ClientHandler.device_websockets[username].append(self.client_socket)


                                # Create a new device object
                                new_device = {
                                    'device_number': device_number,
                                    'device_name': device_name,
                                    'files': files,  # Assuming files is already a list
                                    'storage_capacity_GB': storage_capacity_GB,
                                    'date_added': [date_added], 
                                    'ip_address': ip_address,
                                    'online': True,
                                    'average_upload_speed': average_upload_speed,
                                    'average_download_speed': average_download_speed,
                                    'average_gpu_usage': average_gpu_usage,
                                    'average_cpu_usage': average_cpu_usage,
                                    'average_ram_usage': average_ram_usage,
                                    'upload_network_speed': [float(upload_network_speed)],
                                    'download_network_speed': [float(download_network_speed)],
                                    'gpu_usage': [float(gpu_usage)],
                                    'cpu_usage': [float(cpu_usage)],
                                    'ram_usage': [float(ram_usage)],
                                    'network_reliability': network_reliability,
                                    'average_time_online': average_time_online,
                                    'device_priority': device_priority,
                                    'sync_status': sync_status,
                                    'optimization_status': optimization_status,
                                }
                                device_exists = True
                                devices.append(new_device)

                            # Update the user document with the modified 'devices' array
                            user_collection.update_one({'_id': user['_id']}, {'$set': {'devices': devices}})

                            # Initialize variables
                            number_of_devices = len(devices)
                            number_of_files = 0
                            total_device_storage = 0
                            # Initialize sums for calculating averages
                            total_average_download_speed_sum = 0
                            total_average_upload_speed_sum = 0
                            total_average_gpu_usage_sum = 0
                            total_average_cpu_usage_sum = 0
                            total_average_ram_usage_sum = 0

                            # Iterate through devices to aggregate values
                            for device in devices:
                                number_of_files += len(device.get('files', []))
                                total_device_storage += float(device.get('storage_capacity_GB', 0))
                                total_average_download_speed_sum += float(device.get('average_download_speed', 0))
                                total_average_upload_speed_sum += float(device.get('average_upload_speed', 0))
                                total_average_cpu_usage_sum += float(device.get('average_cpu_usage', 0))
                                total_average_gpu_usage_sum += float(device.get('average_gpu_usage', 0))
                                total_average_ram_usage_sum += float(device.get('average_ram_usage', 0))

                            # Calculate averages, avoid division by zero
                            total_average_download_speed = total_average_download_speed_sum / number_of_devices if number_of_devices > 0 else 0
                            total_average_upload_speed = total_average_upload_speed_sum / number_of_devices if number_of_devices > 0 else 0
                            total_average_cpu_usage = total_average_cpu_usage_sum / number_of_devices if number_of_devices > 0 else 0
                            total_average_gpu_usage = total_average_gpu_usage_sum / number_of_devices if number_of_devices > 0 else 0
                            total_average_ram_usage = total_average_ram_usage_sum / number_of_devices if number_of_devices > 0 else 0

                            user_collection.update_one({'_id': user['_id']}, {'$push': {
                                'number_of_devices': number_of_devices,
                                'number_of_files': number_of_files,
                                'total_device_storage': total_device_storage,
                                'total_average_download_speed': total_average_download_speed,
                                'total_average_upload_speed': total_average_upload_speed,
                                'total_average_cpu_usage': total_average_cpu_usage,
                                'total_average_gpu_usage': total_average_gpu_usage,
                                'total_average_ram_usage': total_average_ram_usage,
                                'overall_date_added': date_added,
                                }})

                            date_time = datetime.now()
                            print(f"{date_time} Data uploaded to Banbury Cloud") 
                            header = None
                            buffer = b""
                            file_type = "Unknown"

                            # except Exception as e:
                                # print(f"Error parsing JSON: {e}")
                    else:
                        print(f"Unknown data type received from {self.client_address}")



                except Exception as e:
                    print(f"we are handling a socket timeout {e}")
                    load_dotenv()
                    uri = os.getenv("MONGODB_URL")
                    client = MongoClient(uri)
                    db = client['myDatabase']
                    user_collection = db['users']
                    for client_socket in list(ClientHandler.device_websockets.values()):
                        if client_socket == self.client_socket:
                            device_name = reverse_lookup(ClientHandler.device_websockets, client_socket)
                            username = reverse_lookup(ClientHandler.device_username, client_socket)
                            # if the username returns none, try another function 
                            if username == None:
                                username = reverse_lookup_list(ClientHandler.device_username, client_socket)
                            if username and device_name:
                                user = user_collection.find_one({'username': username})
                                if user:
                                    devices = user.get('devices', [])
                                    for device in devices:
                                        if device.get('device_name') == device_name:
                                            device['online'] = False
                                            # break
                                    user_collection.update_one({'_id': user['_id']}, {'$set': {'devices': devices}})
                                    print(f"Set {device_name} of {username} to offline")
                            # Remove the socket from the mappings
                            ClientHandler.device_websockets.pop(device_name, None)
                            ClientHandler.device_username.pop(username, None)
                            # ClientHandler.client_addresses.remove(client_socket) 
                            ClientHandler.client_sockets.remove(client_socket)
                        date_time = datetime.now()
                        # print(f"{date_time} All connected client addresses: {ClientHandler.client_addresses}")
        #                 # print(f"{date_time} All connected client devices: {ClientHandler.device_websockets}")
        #                 # print(f"{date_time} All connected client users: {ClientHandler.device_username}")


        except Exception as e:
            print(f"Ping request failed {e}")
            header = None
            buffer = b""


def send_small_ping():
        time.sleep(10)

        date_time = datetime.now()
        # print(f"{date_time} Pinging all devices")
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
                
            # time.sleep(900)
            # time.sleep(30)
            time.sleep(600)


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

