import socket
import threading
import os
from dotenv import load_dotenv
import json
import time
import schedule
from pymongo.mongo_client import MongoClient

SERVER_HOST = '0.0.0.0'  # Server host IP address
SERVER_PORT = 8002  # Server port

class ClientHandler(threading.Thread):
    client_sockets = []
    client_addresses = []
    def __init__(self, client_socket, client_address):
        super().__init__()
        self.client_socket = client_socket
        self.client_address = client_address
        ClientHandler.client_sockets.append(client_socket)
        ClientHandler.client_addresses.append(client_address)

    def run(self):
        end_of_header = b"END_OF_HEADER"
        buffer = b""
        header = None
        file_type = "Unknown"
        while True:
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
                file_size = split_header[2]
                username = split_header[3]
                buffer = content 
            if file_type == "MSG":
                # It's a regular message; process and broadcast it
                message_content = buffer.decode()
                print(f"Received message from {self.client_address}: {message_content}")
                # Broadcast the data to each of the clients in the list of addresses
                for socket in ClientHandler.client_sockets:
                    if socket != self.client_socket:
                        try:
                            socket.sendall(buffer)
                        except Exception as e:
                            print(f"Error sending to client")


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
                            print(f"File Name: {file_name}")
                            file_size = os.path.getsize(file_save_path)
                            print(f"File Size: {file_size}")
                            file_header = f"FILE:{file_name}:{file_size}:"
                            socket.send(file_header.encode())
                            socket.send(b"END_OF_HEADER") # delimiter to notify the server that the header is done

                            with open(file_save_path, 'rb') as file:
                                while True:
                                    bytes_read = file.read(4096)  # Read the file in chunks
                                    if not bytes_read:
                                        break  # File transmission is done
                                    socket.sendall(bytes_read)

                            print(f"{file_name} has been sent successfully.")



                        except Exception as e:
                            print(f"Error sending to device: {e}")


            elif file_type == "FILE_REQUEST":
                print("received FILE_REQUEST")
                directory_name = "BCloud"
                directory_path = os.path.expanduser(f"~/{directory_name}")
                file_save_path = os.path.join(directory_path, file_name)


                print(f"Device is requesting file: {file_name}")
                print(f"Received the request from {self.client_address}: {self.client_socket}")
                # Broadcast the request to each of the clients in the list of addresses
                for socket in ClientHandler.client_sockets:
                    print(socket)
                    if socket != self.client_socket:
                        try:

                            file_header = f"FILE_REQUEST:{file_name}:END_OF_HEADER"
                            print("sending response with file")
                            socket.send(file_header.encode())
                            #socket.send(b"END_OF_HEADER") # delimiter to notify the server that the header is done
                            #socket.sendall(buffer)
                        except Exception as e:
                            print(f"Error sending to device: {e}")

                print("Completed request to device with file, waiting for response...")

       
            elif file_type == "FILE_REQUEST_RESPONSE":
                # It's a file; process the file header to get file info
                print("Received FILE_REQUEST_RESPONSE")
                print(f"Received the request from {self.client_address}: {self.client_socket}")
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

            
                        except BrokenPipeError:
                            print(f"Broken pipe moving on to the next socket.")
                            continue  # This skips the rest of the current iteration and moves to the next socket
                        except Exception as e:
                            print(f"Error sending to device: {e}")

            elif file_type == "FILE_DELETE_REQUEST":
                # It's a file; process the file header to get file info
                print("Received FILE_DELETE_REQUEST")
                print(f"Received the request from {self.client_address}: {self.client_socket}")
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
                            for device in devices:
                                for file in device.get('files', []):
                                    if file.get('File Name') == file_name:
                                        # send a request to that device to delete the file

                                        file_header = f"FILE_DELETE_REQUEST:{file_name}:{file_size}:{username}:END_OF_HEADER"
                                        socket.send(file_header.encode())
                                        print(f"{file_name} has been requested to be deleted")


            
                        except BrokenPipeError:
                            print(f"Broken pipe moving on to the next socket.")
                            continue  # This skips the rest of the current iteration and moves to the next socket
                        except Exception as e:
                            print(f"Error sending to device: {e}")

            
                    else:
                        # TODO: Once all devices confirm that the file doesn't exist, remove it from the database.
                        # Otherwise, the file will be deleted from the database but will still exist on a device.
                        print("No devices to send delete request to. Removing file from database.")
                        # Load Database
                        load_dotenv()
                        uri = os.getenv("MONGODB_URL")

                        client = MongoClient(uri)
                        db = client['myDatabase']
                        user_collection = db['users']
                        user = user_collection.find_one({'username': username})
                           
                        try:
                            # Search each device object in database for a file object that is equal to file_save_path
                            devices = user.get('devices', [])
                            file_removed = False
                            for index, device in enumerate(devices):
                                files_to_remove = [file for file in device.get('files', []) if file.get('File Name') == file_name]
                                for some_file in files_to_remove:
                                    print(f"File detected in database, deleting...")
                                    if any(file['File Name'] == some_file['File Name'] for file in devices[index]['files']):
                                        devices[index]['files'].remove(some_file)  # Add the file if it doesn't exist
                                        user_collection.update_one({'_id': user['_id']}, {'$set': {'devices': devices}})
                                        file_removed = True

                            if file_removed:
                                print(f"{file_name} has been successfully removed from database")
                            else:
                                print(f"{file_name} not found in the database")
                        except BrokenPipeError:
                            print(f"Broken pipe moving on to the next socket.")
                            continue  # This skips the rest of the current iteration and moves to the next socket
                        except Exception as e:
                            print(f"Error removing file from database: {e}")




            elif file_type == "FILE_DELETE_REQUEST_RESPONSE":

                print("Received FILE_DELETE_REQUEST_RESPONSE")
                print(f"Received the request from {self.client_address}: {self.client_socket}")
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
                                    print(f"File detected in database, deleting...")
                                    if any(file['File Name'] == some_file['File Name'] for file in devices[index]['files']):
                                        devices[index]['files'].remove(some_file)  # Add the file if it doesn't exist
                                        user_collection.update_one({'_id': user['_id']}, {'$set': {'devices': devices}})
                                        file_removed = True
                        except BrokenPipeError:
                            print(f"Broken pipe moving on to the next socket.")
                            continue  # This skips the rest of the current iteration and moves to the next socket
                        except Exception as e:
                            print(f"Error sending to device: {e}")




 
            elif file_type == "PING_REQUEST_RESPONSE":

                print("Received ping request response")

                message_content = buffer.decode()
                end_of_JSON = "END_OF_JSON"
                limited_message_content = message_content.split(end_of_JSON)[0]
                print(limited_message_content)
                try:
                    data = json.loads(limited_message_content)
                    
                except json.JSONDecodeError as e:
                    print(f"JSON decode error {e}")
                    data = None
                try:
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



                            # Update existing device in the list
                            devices[index]['upload_network_speed'].append(float(upload_network_speed))
                            devices[index]['download_network_speed'].append(float(download_network_speed))
                            devices[index]['date_added'].append(date_added)
                            print("passed udating existing device")
                            devices[index]['gpu_usage'].append(float(gpu_usage))
                            devices[index]['cpu_usage'].append(float(cpu_usage))
                            devices[index]['ram_usage'].append(float(ram_usage))

                            # Instead of directly appending or extending, check if the file exists
                            for new_file in files:  # Iterate through the new files to be added
                                print(f"new file: {new_file}")
                                # Check if the file already exists in the 'files' array of the device
                                if not any(file['File Name'] == new_file['File Name'] for file in devices[index]['files']):
                                    devices[index]['files'].append(new_file)  # Add the file if it doesn't exist

                            devices[index]['average_upload_speed'] = average_upload_speed
                            devices[index]['average_download_speed'] = average_download_speed
                            devices[index]['average_gpu_usage'] = average_gpu_usage
                            devices[index]['average_cpu_usage'] = average_cpu_usage
                            devices[index]['average_ram_usage'] = average_ram_usage
                            print('updated existing device')
                            device_exists = True
                            break  # Exit loop after updating

                    else:
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


                        # Create a new device object
                        new_device = {
                            'device_number': device_number,
                            'device_name': device_name,
                            'files': files,  # Assuming files is already a list
                            'storage_capacity_GB': storage_capacity_GB,
                            'date_added': [date_added], 
                            'ip_address': ip_address,
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
                        print('added new device')
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


                    print("data uploaded to Banbury Cloud") 
                    header = None
                    buffer = b""

                except Exception as e:
                    print(f"Ping request failed {e}")
                    header = None
                    buffer = b""

            else:
                print(f"Unknown data type received from {self.client_address}")

def send_ping():
        time.sleep(10)
        print("Pinging all devices")
        while True:
            for socket in ClientHandler.client_sockets:
                    print(f"Sending ping request to {socket}")
                    try:
                        null_string = ""
                        file_header = f"PING_REQUEST:{null_string}:{null_string}:END_OF_HEADER"
                        socket.send(file_header.encode())
                        #socket.send(b"END_OF_HEADER") # delimiter to notify the server that the header is done
       
                    except BrokenPipeError:
                        print(f"Broken pipe moving on to the next socket.")
                        continue  # This skips the rest of the current iteration and moves to the next socket
                    except Exception as e:
                        print(f"Error sending to device: {e}")
            time.sleep(900)
def main():
    # Create a server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")
    client_sockets = []
    client_addresses = []
    running = True
    try:
        threading.Thread(target=send_ping, daemon=True).start()
        while running:
            # Accept incoming connections
            schedule.run_pending()
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address}")
            # Start a new thread to handle the client
            client_handler = ClientHandler(client_socket, client_address)
            client_handler.start()
            print(f"All connected client addresses: {ClientHandler.client_addresses}")
    except KeyboardInterrupt:
        print("Server shutting down...")
        running = False
        for client_socket in ClientHandler.client_sockets:
            client_socket.close()
        server_socket.close()
    finally:
        server_socket.close()
        print("Server has been shut down.")

if __name__ == "__main__":
    main()

