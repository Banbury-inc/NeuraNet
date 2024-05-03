# login_handler.py

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime
import bcrypt

class FileHandler:
    def __init__(self, client_socket):
        self.client_socket = client_socket

    def process_file(self, buffer, username, password, file_name, device_name, file_size):

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
    def process_file_request(self, buffer, username, password, file_name, device_name, file_size):
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
    def process_file_request_response(self, buffer, username, password, file_name, device_name, file_size):
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
    def process_file_delete_request(self, buffer, username, password, file_name, device_name, file_size):

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
            # continue  # This skips the rest of the current iteration and moves to the next socket
        except Exception as e:
            print(f"Error removing file from database: {e}")

    def process_file_delete_request_response(self, buffer, username, password, file_name, device_name, file_size):
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

