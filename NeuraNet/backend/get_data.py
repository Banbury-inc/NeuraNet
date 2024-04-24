
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def create_dataset(X, y, time_steps=1):
    Xs, ys = [], []
    for i in range(len(X) - time_steps):
        v = X.iloc[i:(i + time_steps)].values
        Xs.append(v)
        ys.append(y.iloc[i + time_steps])
    return np.array(Xs), np.array(ys)


# Load environment variables (assuming you have them set up for MongoDB access)
load_dotenv()
uri = os.getenv("MONGODB_URL")

# Connect to MongoDB
client = MongoClient(uri)
db = client['myDatabase']
user_collection = db['users']

# Get user data (assuming 'username' is defined elsewhere)
username = "mmills6060"  # Replace with your username
user = user_collection.find_one({'username': username})

devices = user.get('devices', [])

# Initialize variables to store resource usage
total_upload_speed = 0
total_download_speed = 0
total_gpu_usage = 0
total_cpu_usage = 0
total_ram_usage = 0

# Counters for resource usage data
upload_speed_count = 0
download_speed_count = 0
gpu_usage_count = 0
cpu_usage_count = 0
ram_usage_count = 0

device_info_list = []
# Process device data
# Process device data
for device in devices:
    device_name = device.get('device_name', 'Unknown Device')
    upload_speeds = [float(speed) for speed in device.get('upload_network_speed', []) if isinstance(speed, (int, str, float)) and speed != '']
    download_speeds = [float(speed) for speed in device.get('download_network_speed', []) if isinstance(speed, (int, str, float)) and speed != '']
    gpu_usages = [float(usage) for usage in device.get('gpu_usage', []) if isinstance(usage, (int, str, float)) and usage != '']
    cpu_usages = [float(usage) for usage in device.get('cpu_usage', []) if isinstance(usage, (int, str, float)) and usage != '']
    ram_usages = [float(usage) for usage in device.get('ram_usage', []) if isinstance(usage, (int, str, float)) and usage != '']
    date_added = [datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S.%f") for date_string in device.get('date_added', []) if date_string]

    device_info = {
        'device_name': device_name,
        'upload_speeds': upload_speeds,
        'download_speeds': download_speeds,
        'gpu_usages': gpu_usages,
        'cpu_usages': cpu_usages,
        'ram_usages': ram_usages,
        'date_added': [date.strftime('%Y-%m-%d %H:%M:%S') for date in date_added]  # readable date formats
    }
    
    device_info_list.append(device_info)  # Append the device information to the list

# Display the collected device information
for device_data in device_info_list:
    print(device_data['device_name'])
    print(f"Upload Speeds: {device_data['upload_speeds']}")
    print(f"Download Speeds: {device_data['download_speeds']}")
    print(f"GPU Usages: {device_data['gpu_usages']}")
    print(f"CPU Usages: {device_data['cpu_usages']}")
    print(f"RAM Usages: {device_data['ram_usages']}")
    print(f"Date Added: {device_data['date_added']}")
    print("\n")  # Add a new line for better readability between devices


