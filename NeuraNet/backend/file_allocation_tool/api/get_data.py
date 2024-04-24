import os
from dotenv import load_dotenv
from pymongo import MongoClient

class Get():
    def __init__(self):
        pass
    def devices(self):

        # Load environment variables
        load_dotenv()
        uri = os.getenv("MONGODB_URL")
        client = MongoClient(uri)
        db = client['myDatabase']
        user_collection = db['users']
        username = "mmills6060"
        user = user_collection.find_one({'username': username})
        devices = user.get('devices', [])

        return devices

