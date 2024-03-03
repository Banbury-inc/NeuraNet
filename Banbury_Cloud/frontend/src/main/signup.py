import sys
import os
from dotenv import load_dotenv
import pymongo
import bcrypt
from pymongo.server_api import ServerApi

def signup(name, username, password_str):
    # Hash the password
    password_bytes = password_str.encode('utf-8')  # Encode the string to bytes
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    # Connect to MongoDB
    load_dotenv()
    uri = os.getenv("MONGODB_URL")
    client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
    db = client['myDatabase']
    user_collection = db['users']

    # Check if the username already exists
    existing_user = user_collection.find_one({'username': username})
    if existing_user:
        print("Username already exists. Please choose another one.")
        return

    # Insert the new user into the database
    user_data = {
        'name': name,
        'username': username,
        'password': hashed_password
    }
    user_collection.insert_one(user_data)
    print("Signup successful!")

def main():
    if len(sys.argv) > 1:
        # Expecting name, username, and password as command line arguments
        name = sys.argv[1]
        username = sys.argv[2]
        password_str = sys.argv[3]
        signup(name, username, password_str)
    else:
        print("No argument received. Usage: python your_script.py <name> <username> <password>")

if __name__ == "__main__":
    main()
