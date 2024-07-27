import os
from dotenv import load_dotenv
from pymongo import MongoClient
import certifi
class Get():
    def __init__(self):
        load_dotenv()  # It's better to load environment variables once in the initializer
        uri = "mongodb+srv://mmills6060:Dirtballer6060@banbury.fx0xcqk.mongodb.net/?retryWrites=true&w=majority"
        # self.client = MongoClient(uri)
        self.client = MongoClient(uri, tlsCAFile=certifi.where())
        self.db = self.client['myDatabase']
        self.user_collection = self.db['users']
    
    def devices(self):
        username = "mmills6060"
        # username = "null"
        user = self.user_collection.find_one({'username': username})
        return user.get('devices', [])
    
    def files(self):
        devices = self.devices()
        all_files = []

        # Iterate over each device and extract files
        for device in devices:
            device_files = device.get('files', [])  # Ensure there's a 'files' key in the device document
            for file in device_files:
                # Validate the expected keys in each file dictionary
                if 'File Name' in file and 'File Size' in file:
                    all_files.append({
                        'file_name': file['File Name'],
                        'priority': "high",
                        'size': file['File Size']
                    })
        
        return all_files



