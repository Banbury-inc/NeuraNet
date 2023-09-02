import subprocess
import hashlib
import uuid
import json
from flask import Flask, Response, jsonify, request, render_template, redirect, url_for
import devices





app = Flask(__name__)
devices_list = []
def register_user(username, password, first_name, last_name):
    user_id = generate_user_id()

    # Hash the password before storing it
    hashed_password = hash_password(password)

    # Create a JSON object with user information
    user_data = {
        "user_id": user_id,
        "username": username,
        "hashed_password": hashed_password,
        "first_name" : first_name,
        "last_name" : last_name,
        "devices" : devices_list
    }
    json_str = json.dumps(user_data)

    # Connect to IPFS node
#   devices.connect_device_to_ipfs()

    # initialize IPFS node

    devices.initialize_IPFS()

    try:
        # Run the IPFS command-line interface to add the JSON data
        completed_process = subprocess.run(["ipfs", "add", "-Q"], input=json_str, capture_output=True, text=True, check=True)

        # Get the CID (content identifier) from the command output
        cid = completed_process.stdout.strip()
        return cid
    except subprocess.CalledProcessError as e:
        print("Failed to add JSON to IPFS:", e)
        return None

def hash_password(password):
    # Use a secure hashing algorithm, such as SHA-256
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username, password):
    # Get the CID for the user data using the username as a key
    cid = lookup_user_data_cid(username)

    if cid:
        # Retrieve the user data from IPFS
        user_data = get_from_ipfs(cid)

        # Hash the provided password and compare it with the stored hashed password
        hashed_password = hash_password(password)
        if user_data and user_data["hashed_password"] == hashed_password:
            return user_data["user_id"], user_data["username"], user_data["first_name"], user_data["last_name"], user_data["devices"]

    # Authentication failed
    return None

def lookup_user_data_cid(username):
    # Implement a lookup method to find the CID associated with the username
    # For example, you could use a database or another IPFS object that maps usernames to CIDs.
    # In this example, we assume the data is in a dictionary named 'user_data_mapping'.
    user_data_mapping = {
        "john_doe": "QmWWAwkSLNi2q77T7CWPohByoKV9dsyHRrDLbtTHSwRpHE",
        "mmills6060": "QmWZGCi5Bnn89pQWmFYqhEBHRkfimBhCVwmUoAztEmh8B8",
        # ...
    }
    return user_data_mapping.get(username)

def generate_user_id():
    # Generate a UUIDv4 (random-based) user ID
    return str(uuid.uuid4())

def add_to_ipfs(data):
    try:
        completed_process = subprocess.run(['ipfs', 'add', '-Q'], input=data.encode(), capture_output=True, text=True, check=True)
        cid = completed_process.stdout.strip()
        return cid
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        print("Command output:", e.output)
        return None

def get_from_ipfs(cid):
    # Use subprocess to get data from IPFS using the 'ipfs cat' command
    completed_process = subprocess.run(['ipfs', 'cat', cid], capture_output=True, text=True)
    # Get the data from the output
    data = completed_process.stdout.strip()
    if data:
        # Parse the JSON data
        return json.loads(data)
    return None


def usage_example():
    # Registration Example
    username = "mmills6060"
    password = "password"
    first_name = "Michael" 
    last_name = "Mills"
    user_cid = register_user(username, password, first_name, last_name)
    print("User registered with CID:", user_cid)

    # Authentication Example
    username = "john_doe"
    password = "secretpassword"
    user_id = authenticate_user(username, password)

    if user_id:
        print("User authenticated. User ID:", user_id)
    else:
        print("Authentication failed. Invalid username or password.")






def main():
    
    # Authentication Example
    username = "mmills6060"
    password = "password"
    user_data = authenticate_user(username, password)
    print(user_data)
    

if __name__ == "__main__":
    main()
    
