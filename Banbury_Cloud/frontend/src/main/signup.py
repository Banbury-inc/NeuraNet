import sys
import os
from dotenv import load_dotenv
import pymongo
import bcrypt
from pymongo.server_api import ServerApi

def signup(username, password_str, email="", firstname="", lastname="", phone_number=""):
    # Check if username and password are provided
    if not username or not password_str:
        print("Username and password are required fields.")
        return

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
        'username': username,
        'password': hashed_password,
        'email': email,
        'firstname': firstname,
        'lastname': lastname,
        'phone_number': phone_number
    }
    user_collection.insert_one(user_data)
    print("Signup successful!")

def main():
    if len(sys.argv) > 1:
        # Expecting username and password as compulsory arguments
        username = sys.argv[1]
        password_str = sys.argv[2]
        # Optional arguments
        email = sys.argv[3] if len(sys.argv) > 3 else ""
        firstname = sys.argv[4] if len(sys.argv) > 4 else ""
        lastname = sys.argv[5] if len(sys.argv) > 5 else ""
        phone_number = sys.argv[6] if len(sys.argv) > 6 else ""
        signup(username, password_str, email, firstname, lastname, phone_number)
    else:
        print("No argument received. Usage: python your_script.py <username> <password> [<email> <firstname> <lastname> <phone_number>]")

if __name__ == "__main__":
    main()
