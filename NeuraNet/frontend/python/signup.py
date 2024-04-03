import sys
import os
import json
import requests
from dotenv import load_dotenv
import bcrypt

def signup(username, password_str, firstname="", lastname=""):
    # Check if username and password are provided
    if not username or not password_str:
        print("Username and password are required fields.")
        return

    # Hash the password
    password_bytes = password_str.encode('utf-8')  # Encode the string to bytes
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())


    # Make the API call to register the user
    response = requests.get('https://website2-v3xlkt54dq-uc.a.run.app/register/' + firstname + '/' + lastname + '/' + username + '/' + password_str + '/')

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
        result = "success"
        return result
    else:
        print("User registration failed:", response.text)
        result = "fail"
        return result

def main():
    if len(sys.argv) > 1:
        # Expecting username and password as compulsory arguments
        username = sys.argv[1]
        password_str = sys.argv[2]
        # Optional arguments
        firstname = sys.argv[3] if len(sys.argv) > 3 else ""
        lastname = sys.argv[4] if len(sys.argv) > 4 else ""
        result = signup(username, password_str, firstname, lastname)
        print(f"Result: {result}")
    else:
        username = "testuser"
        password_str = "testuser"
        firstname = "firstname"
        lastname = "lastname"
        result = signup(username, password_str, firstname, lastname)
        print(f"Result: {result}")
 
if __name__ == "__main__":
    main()
