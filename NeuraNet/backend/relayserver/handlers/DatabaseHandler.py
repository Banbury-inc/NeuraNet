# login_handler.py

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime
import bcrypt

class DatabaseHandler:
    def __init__(self):
        pass
    def initialize(self):
        load_dotenv()
        uri = os.getenv("MONGODB_URL")
        client = MongoClient(uri, tlsAllowInvalidCertificates=True)
        db = client['myDatabase']
        user_collection = db['users']
        for user in user_collection.find():
            if user:
                devices = user.get('devices', [])
                for device in devices:
                    device['online'] = False
                user_collection.update_one({'_id': user['_id']}, {'$set': {'devices': devices}})

    def get_devices(self, username):
        uri = os.getenv("MONGODB_URL")
        client = MongoClient(uri, tlsAllowInvalidCertificates=True)
        db = client['myDatabase']
        user_collection = db['users']
        user = user_collection.find_one({'username': username})
        devices = user.get('devices', [])
        return devices

    def get_user(self, username):
        uri = os.getenv("MONGODB_URL")
        client = MongoClient(uri, tlsAllowInvalidCertificates=True)
        db = client['myDatabase']
        user_collection = db['users']
        user = user_collection.find_one({'username': username})
        return user

    def update_devices(self, username, devices):
        uri = os.getenv("MONGODB_URL")
        client = MongoClient(uri, tlsAllowInvalidCertificates=True)
        db = client['myDatabase']
        user_collection = db['users']
        user = user_collection.find_one({'username': username})
        user_collection.update_one({'_id': user['_id']}, {'$set': {'devices': devices}})
        return

    def update_device_numbers(self, devices):
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
        return devices
    def append_device_info(self,
                               index, 
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
                              date_added
                           ):

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


            def safe_append(device_dict, key, value):
                """
                Safely append a value to a list in the dictionary. If the key doesn't exist,
                it initializes a new list. If the value conversion fails, it logs the error.
                """
                try:
                    if key not in device_dict:
                        device_dict[key] = []
                    device_dict[key].append(value)
                except ValueError as e:
                    print(f"Error converting {value} for {key}: {str(e)}")
                except Exception as e:
                    print(f"Unexpected error when updating {key} with {value}: {str(e)}")


            try:
                device_dict = devices[index]
                # Safely append data
                safe_append(device_dict, 'upload_network_speed', float(upload_network_speed))
                safe_append(device_dict, 'download_network_speed', float(download_network_speed))
                safe_append(device_dict, 'date_added', date_added)  # Assuming date_added is already correct format
                safe_append(device_dict, 'gpu_usage', float(gpu_usage))
                safe_append(device_dict, 'cpu_usage', float(cpu_usage))
                safe_append(device_dict, 'ram_usage', float(ram_usage))
                safe_append(device_dict, 'predicted_upload_network_speed', float(predicted_upload_network_speed))
                safe_append(device_dict, 'predicted_download_network_speed', float(predicted_download_network_speed))
                safe_append(device_dict, 'predicted_gpu_usage', float(predicted_gpu_usage))
                safe_append(device_dict, 'predicted_cpu_usage', float(predicted_cpu_usage))
                safe_append(device_dict, 'predicted_ram_usage', float(predicted_ram_usage))
                safe_append(device_dict, 'predicted_performance_score', float(predicted_performance_score))
                # Non-appending assignments can simply check for KeyError or TypeError
                device_dict['files'] = files
                device_dict['tasks'] = tasks
                device_dict['average_upload_speed'] = average_upload_speed
                device_dict['average_download_speed'] = average_download_speed
                device_dict['average_gpu_usage'] = average_gpu_usage
                device_dict['average_cpu_usage'] = average_cpu_usage
                device_dict['average_ram_usage'] = average_ram_usage
                device_dict['online'] = True
                device_exists = True
            except KeyError as e:
                print(f"Missing required field: {str(e)}")
            except Exception as e:
                print(f"An error occurred updating the device: {str(e)}")





        return devices

    def add_new_device(self, data, 
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
                       optimization_status):

        upload_speeds = [data["upload_network_speed"]]
        download_speeds = [data["download_network_speed"]]
        gpu_usages = [data["gpu_usage"]]
        cpu_usages = [data["cpu_usage"]]
        ram_usages = [data["ram_usage"]]
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
            'max_storage_capacity_GB': max_storage_capacity_GB,
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
            'predicted_upload_network_speed': [float(predicted_upload_network_speed)],
            'predicted_download_network_speed': [float(predicted_download_network_speed)],
            'predicted_gpu_usage': [float(predicted_gpu_usage)],
            'predicted_cpu_usage': [float(predicted_cpu_usage)],
            'predicted_ram_usage': [float(predicted_ram_usage)],
            'predicted_performance_score': [float(predicted_performance_score)],
            'network_reliability': network_reliability,
            'average_time_online': average_time_online,
            'tasks': [float(tasks)],
            'device_priority': device_priority,
            'sync_status': sync_status,
            'optimization_status': optimization_status,
        }
        device_exists = True
        devices.append(new_device)
        return devices

    def update_user_metrics(self, devices, user, date_added, username):

        uri = os.getenv("MONGODB_URL")
        client = MongoClient(uri, tlsAllowInvalidCertificates=True)
        db = client['myDatabase']
        user_collection = db['users']
        user = user_collection.find_one({'username': username})
 
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




