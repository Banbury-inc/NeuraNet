import sys
import os
import json
import requests
from dotenv import load_dotenv
import bcrypt

def signup(username, password_str, email="", firstname="", lastname="", phone_number=""):
    # Check if username and password are provided
    if not username or not password_str:
        print("Username and password are required fields.")
        return

    # Hash the password
    password_bytes = password_str.encode('utf-8')  # Encode the string to bytes
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    # Prepare the data for the API call
    data = {
       'firstName': firstname,
        'lastName': lastname,
        'username': username,
        'password': hashed_password.decode(),  # Convert bytes to string for JSON serialization
 
    }

    # Make the API call to register the user
    response = requests.post('https://website2-v3xlkt54dq-uc.a.run.app/register', json=data)

    # Check if the request was successful
    if response.status_code == 200:
        print("User registration successful!")

        # Add credentials to credentials.json in banbury
        credentials = {
            'username': username,
            'password': password_str  # Storing plaintext password for demonstration, use with caution
        }
        with open('banbury/credentials.json', 'w') as f:
            json.dump(credentials, f)
        print("Credentials added to credentials.json in banbury.")
    else:
        print("User registration failed:", response.text)


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
