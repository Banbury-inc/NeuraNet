# login_handler.py

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime
import bcrypt
import json
import threading
import time
from .DatabaseHandler import DatabaseHandler
from utils.Lookup import Lookup

class PingHandler:
    def __init__(self, client_address, client_socket, client_sockets, device_username):
        self.client_address = client_address
        self.client_socket = client_socket
        self.client_sockets = client_sockets
        # self.device_username = client_sockets
        self.device_username = device_username


    def process_small_ping_request_response(self, total_json, username, password, file_name, device_name, file_size):
            try:
                data = json.loads(total_json)  # Parsing string to JSON
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
            # ClientHandler.device_websockets[device_name] = self.client_socket

            if username in self.device_username:
                # if the device is already appended to the list of devices, do nothing
                if self.client_socket not in self.device_username[username]:
                    print("current socket not in list of devices, adding")
                    self.device_username[username].append(self.client_socket)
            else:
                self.device_username[username] = [self.client_socket]


            database = DatabaseHandler()
            devices = database.get_devices(username)

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


            device_exists = False
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

            if not device_exists:
                # If the device name doesn't match any of the user's devices in the database, send ping
                print(f"Device {device_name} not found in database, sending ping request")
                result = "device_not_found"
                return result

            database.update_devices(username, devices)
            # Iterate through devices to aggregate values
            date_time = datetime.now()
            # print(f"{date_time} Data uploaded to Banbury Cloud") 
            header = None
            buffer = b""
            file_type = "Unknown"

            # except Exception as e:
                # print(f"Error parsing JSON: {e}")


            # If the device name doesn't match any of the user's devices in the database, send ping
            
            return self.client_socket

    def process_ping_request_response(self, total_json, username, password, file_name, device_name, file_size):

            try:
                data = json.loads(total_json)  # Parsing string to JSON
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
            max_storage_capacity_GB = data["max_storage_capacity_GB"]
            date_added = data["date_added"]
            ip_address = data["ip_address"]
            average_network_speed = data["average_network_speed"]
            upload_network_speed = data["upload_network_speed"]
            download_network_speed = data["download_network_speed"]
            gpu_usage = data["gpu_usage"]
            cpu_usage = data["cpu_usage"]
            ram_usage = data["ram_usage"]
            predicted_upload_network_speed = data["predicted_upload_network_speed"]
            predicted_download_network_speed = data["predicted_download_network_speed"]
            predicted_gpu_usage = data["predicted_gpu_usage"]
            predicted_cpu_usage = data["predicted_cpu_usage"]
            predicted_ram_usage = data["predicted_ram_usage"]
            predicted_performance_score = data["predicted_performance_score"]
            network_reliability = data["network_reliability"]
            average_time_online = data["average_time_online"]
            tasks = data["tasks"]
            device_priority = data["device_priority"]
            sync_status = data["sync_status"]
            optimization_status = data["optimization_status"]


            #stay away from this shit
            # ClientHandler.device_websockets[device_name] = self.client_socket

            if username in self.device_username:
                # if the device is already appended to the list of devices, do nothing
                if self.client_socket not in self.device_username[username]:
                    print("current socket not in list of devices, adding")
                    self.device_username[username].append(self.client_socket)
            else:
                self.device_username[username] = [self.client_socket]

            # print(f"{date_time} All connected devices: {ClientHandler.device_websockets}")
            # print(f"{date_time} All connected users: {ClientHandler.device_username}")
            database = DatabaseHandler()
            user = database.get_user(username)
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

            database.update_device_numbers(devices)
            for index, device in enumerate(devices):
                if device.get('device_name') == device_name:
                    devices = database.append_device_info(index, 
                                                          device, 
                                                          devices, 
                                                          device_name, 
                                                          upload_network_speed, 
                                                          download_network_speed, 
                                                          gpu_usage, 
                                                          cpu_usage, 
                                                          ram_usage, 
                                                          predicted_upload_network_speed, 
                                                          predicted_download_network_speed, 
                                                          predicted_gpu_usage, 
                                                          predicted_cpu_usage, 
                                                          predicted_ram_usage, 
                                                          predicted_performance_score, 
                                                          files, 
                                                          tasks,
                                                          date_added)
                    break
            else:
                print("Device not found, creating new device")

                devices = database.add_new_device(data, 
                       devices, 
                       device_number, 
                       device_name, 
                       upload_network_speed, 
                       download_network_speed, 
                       gpu_usage, 
                       cpu_usage, 
                       ram_usage, 
                       predicted_upload_network_speed, 
                       predicted_download_network_speed, 
                       predicted_gpu_usage, 
                       predicted_cpu_usage, 
                       predicted_ram_usage, 
                       predicted_performance_score,
                       files, 
                       storage_capacity_GB, 
                       max_storage_capacity_GB, 
                       date_added, 
                       ip_address, 
                       network_reliability, 
                       average_time_online, 
                       tasks, 
                       device_priority, 
                       sync_status, 
                       optimization_status)
            # Update the user document with the modified 'devices' array
            database.update_devices(username, devices)
            database.update_user_metrics(devices, user, date_added, username)


            date_time = datetime.now()
            print(f"{date_time} Data uploaded to Banbury Cloud") 
            header = None
            buffer = b""
            file_type = "Unknown"

            # except Exception as e:
                # print(f"Error parsing JSON: {e}")

            return self.client_socket

