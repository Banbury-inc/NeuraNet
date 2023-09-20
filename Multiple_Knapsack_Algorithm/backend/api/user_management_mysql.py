import subprocess
import hashlib
import uuid
import json
import requests
# from scan_files import file_info_list
from flask import Flask, Response, jsonify, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy






app = Flask(__name__)

# Configure SQLAlchemy for MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://mmills6060:Dirtballer!6060@localhost:3306/banburye_users'
db = SQLAlchemy(app)

devices_list = []
files_cid_list = []
new_user_cid = []


# Define the user_data_mapping dictionary
user_data_mapping = {
    "john_doe": "QmWWAwkSLNi2q77T7CWPohByoKV9dsyHRrDLbtTHSwRpHE",
    "mmills6060": "QmbUUSr7XXWcBy5d6kMTqXYnUQuPze59xm6vKxmeKvcAq7",
    "pointblank6060": "QmNQZcjxADKRdXfccd3uz6rs7tf6G9EF2m66QiGPGwUjkE",
    "pointblank606060": "QmVTYBc56oBikLmnvJyEFiVimt3MjGVx6kRbrQtpqPpzyn",
    "pointblank60606060": "QmUP5JT35LPsqMjZ9a32KMVf4SZMri3XbFTpjGWbarCgz3",
    "pointblank": "QmfRu8KEc3EjhQjQYZvKqz2R3if7NpVuUa55Uk4pB6zMzN",
    "bruh": "QmUzd26tQXDectQAVNgLzdWQzPkzJnc9aLsYkcy6YYFVPK",
    "sad": "QmZZXQhoLuFUv7EXVmhkpkPws1G5zCzkUE25giB8CuR3nB",
    "yup": "QmRx5SuUQpKvPAeVHBHduynkLoFQipfDwgjT9kNjH7DAew"
    # ...

}

def test_database_connection():
    """Tests the connection to the database.

    Returns:
        A string message indicating whether the connection was successful or not.
    """

    try:
        # Try to create a connection to the database
        db.session.connection()

        # If the connection is successful, return a success message
        return "Database connection successful!"
    except Exception as e:
        # If the connection fails, return an error message
        return f"Database connection failed: {str(e)}"


def print_user_data_map():
    # get the user data map from http://127.0.0.1:5000/users
    # URL of the JSON data
    url = "http://127.0.0.1:5000/users"

    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON data from the response
            user_data = response.json()


        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    
    # Convert user_data to a string

    user_data_string = str(user_data[0])
    completed_process = subprocess.run(["ipfs", "cat", user_data_string], capture_output=True, text=True, check=True)
    existing_data = json.loads(completed_process.stdout)
    print(existing_data)

def get_user_data_map():
        
    # get the user data map from http://127.0.0.1:5000/users
    # URL of the JSON data
    url = "http://127.0.0.1:5000/users"

    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON data from the response
            user_data = response.json()

        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    
    # Convert user_data to a string
    print("")
    print(user_data)
    print("")
    user_data_string = str(user_data[0])
    completed_process = subprocess.run(["ipfs", "cat", user_data_string], capture_output=True, text=True, check=True)
    existing_data = json.loads(completed_process.stdout)
    return existing_data

# Update the existing_data dictionary in update_user_data_map
def update_user_data_map_with_arguments(username, cid):
    # Get the existing data
    existing_data = get_user_data_map()

    
    # Check if the username already exists in the dictionary
    if username in existing_data:
        # If it exists, append the new CID to the list of CIDs for that username
        existing_data[username].append(cid)
    else:
        # If it doesn't exist, create a new entry with a list containing the CID
        existing_data[username] = [cid]

    json_str = json.dumps(existing_data)
    print(json_str)

    try:
        # Run the IPFS command-line interface to add the JSON data
        completed_process = subprocess.run(["ipfs", "add", "-Q"], input=json_str, capture_output=True, text=True, check=True)

        # Get the CID (content identifier) from the command output
        cid = completed_process.stdout.strip()

        return cid

    except subprocess.CalledProcessError as e:
        print("Failed to add JSON to IPFS:", e)
        return None


# Update the existing_data dictionary in update_user_data_map
def update_user_data_map():
    # Get the existing data
    existing_data = get_user_data_map()
    username = "pdins"
    cid = "QmVVN534uiN2Zrddd2rssidTkmcUoQH898YmSbtki8FjynLh"
    
    # Check if the username already exists in the dictionary
    if username in existing_data:
        # If it exists, append the new CID to the list of CIDs for that username
        existing_data[username].append(cid)
    else:
        # If it doesn't exist, create a new entry with a list containing the CID
        existing_data[username] = [cid]

    json_str = json.dumps(existing_data)
    print(json_str)

    try:
        # Run the IPFS command-line interface to add the JSON data
        completed_process = subprocess.run(["ipfs", "add", "-Q"], input=json_str, capture_output=True, text=True, check=True)

        # Get the CID (content identifier) from the command output
        cid = completed_process.stdout.strip()

        return cid

    except subprocess.CalledProcessError as e:
        print("Failed to add JSON to IPFS:", e)
        return None

# In update_user_data_map_cid, handle the response and update your data
def update_user_data_map_cid_with_arguments(username, cid):

    # Construct the URL with variables
    url = f"http://127.0.0.1:5000/update_users_with_arguments?username={username}&cid={cid}"

    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON data from the response
            user_data = response.json()

            # Update your data map with the received data
            global next_user_data_map
            next_user_data_map = user_data

        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


# In update_user_data_map_cid, handle the response and update your data
def update_user_data_map_cid():
    url = "http://127.0.0.1:5000/update_users"

    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON data from the response
            user_data = response.json()

            # Update your data map with the received data
            global next_user_data_map
            next_user_data_map = user_data

        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


def register_user_add_to_user_data_map(username, password, first_name, last_name, devices_list, file_info_list):
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
        "devices" : devices_list,
        "files" : file_info_list
    }
    json_str = json.dumps(user_data)

    # Connect to IPFS node
#   devices.connect_device_to_ipfs()

    # initialize IPFS node

#    devices.initialize_IPFS()

    try:
        # Run the IPFS command-line interface to add the JSON data
        completed_process = subprocess.run(["ipfs", "add", "-Q"], input=json_str, capture_output=True, text=True, check=True)

        # Get the CID (content identifier) from the command output
        cid = completed_process.stdout.strip()


        update_user_data_map_cid_with_arguments(username, cid)

        return cid
    except subprocess.CalledProcessError as e:
        print("Failed to add JSON to IPFS:", e)
        return None




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
        "devices" : devices_list,
        "files" : file_info_list
    }
    json_str = json.dumps(user_data)

    # Connect to IPFS node
#   devices.connect_device_to_ipfs()

    # initialize IPFS node

#    devices.initialize_IPFS()

    try:
        # Run the IPFS command-line interface to add the JSON data
        completed_process = subprocess.run(["ipfs", "add", "-Q"], input=json_str, capture_output=True, text=True, check=True)

        # Get the CID (content identifier) from the command output
        cid = completed_process.stdout.strip()

        

        return cid
    except subprocess.CalledProcessError as e:
        print("Failed to add JSON to IPFS:", e)
        return None


def update_user_info(username, password, updated_info):
    # Fetch the existing user data from IPFS based on user_id
    existing_data_cid = authenticate_user(username, password)

    if existing_data_cid is None:
        print("User not found.")
        return None

    try:
        # Fetch the existing JSON data from IPFS
        completed_process = subprocess.run(["ipfs", "cat", existing_data_cid], capture_output=True, text=True, check=True)

        # Parse the existing JSON data
        existing_data = json.loads(completed_process.stdout)

        # Update user information with the provided updated_info
        existing_data.update(updated_info)

        # Convert the updated user data back to JSON
        updated_json_str = json.dumps(existing_data)
        cid = get_user_cid_from_username(username)

        # Run IPFS to remove the data associated with the CID
        subprocess.run(["ipfs", "pin", "rm", cid], check=True)


        # Run IPFS to add the updated JSON data
        completed_process = subprocess.run(["ipfs", "add", "-Q"], input=updated_json_str, capture_output=True, text=True, check=True)

        # Get the new CID after the update
        updated_cid = completed_process.stdout.strip()
        print(updated_cid)
        return updated_cid
    except subprocess.CalledProcessError as e:
        print("Failed to update user info in IPFS:", e)
        return None
    

def hash_password(password):
    # Use a secure hashing algorithm, such as SHA-256
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username, password):
    # Get the CID for the user data using the username as a key
    cid = lookup_cid_from_username(username)

    if cid:
        # Retrieve the user data from IPFS
        user_data = get_from_ipfs(cid)

        # Hash the provided password and compare it with the stored hashed password
        hashed_password = hash_password(password)
        if user_data and user_data["hashed_password"] == hashed_password:
            return user_data["user_id"], user_data["username"], user_data["first_name"], user_data["last_name"], user_data["devices"], user_data["files"]

    # Authentication failed
    return None
def get_user_cid_from_username(username):
    # Get the CID for the user data using the username as a key
    cid = lookup_cid_from_username(username)

    if cid:
        return cid
    # Authentication failed
    return None

def lookup_cid_from_username(username):


    return user_data_mapping.get(username)

def lookup_username_from_cid(cid):


    # Search for the username associated with the given CID
    for username, stored_cid in user_data_mapping.items():
        if stored_cid == cid:
            return username

    return None



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


def username_exists(username):

    
    # Check if the provided CID exists in the user_data_mapping dictionary
    return username in user_data_mapping




def main():
    
    message = test_database_connection()
    print(message)

 

if __name__ == "__main__":
    main()
    
