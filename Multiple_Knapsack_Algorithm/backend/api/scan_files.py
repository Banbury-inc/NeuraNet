import os
#from decentralized_storage import ipfs
import json
import subprocess


file_info = []
new_user_cid = []
list_cid_for_file_info = []
list_cid_for_file_content = []
file_info_list = []

def scan_folder(folder_path, username, password, first_name, last_name):
    file_list = []

    for entry in os.scandir(folder_path):
        if entry.is_file():
            file_content = get_file_content(username, password, first_name, last_name, entry.path, priority="high")
            if file_content is not None:
                list_cid_for_file_content.append(file_content)
        elif entry.is_dir():
            print("Directory:", entry.name)
            list_cid_for_file_content.extend(scan_folder(entry.path))

    return file_info_list

def get_file_content(username, password, first_name, last_name, file_path, priority="normal"):
    from backend.api import user_management
    from backend.api.user_management import user_data_mapping

    if not os.path.exists(file_path):
        return None


    # Generate CID for the file using IPFS
    cid_for_file_content = ipfs_add(file_path)

    # Add CID to files_cid_list
    user_management.files_cid_list.append(cid_for_file_content)
    list_cid_for_file_content.append(cid_for_file_content)



    cid_for_file_info = get_info_of_file(file_path, cid_for_file_content)

    # search to see if username already exists
    exists = user_management.username_exists(username)
    old_cid = user_management.lookup_cid_from_username
    # if username exists, erase the previous CID associated with the username
    if exists == True:
        # erase the previous CID associated with the username
        remove_cid_from_ipfs(old_cid)
        #remove the previous element containing old username from dictionary
        
            
        del user_management.user_data_mapping[username]
        
        # update the CID associated with the username
        new_user_cid = user_management.register_user(username, password, first_name, last_name)

        # add the new element with the specified username and CID

        user_management.user_data_mapping[username] = new_user_cid
    # if username does not exist, create a new CID for the user
    else:
        new_user_cid = user_management.register_user(username, password, first_name, last_name)
    # Delete all elements from new_user_cid using clear()
    user_management.new_user_cid.clear()
    # Add user CID to new_user_cid
    user_management.new_user_cid.append(new_user_cid)


    return cid_for_file_info, cid_for_file_content    
    


def get_info_of_file(file_path, cid_for_file_content):
    if not os.path.exists(file_path):
        return None

    file_id = hash(file_path)  # You can use a hash of the file path as an identifier
    file_name = os.path.basename(file_path)
    file_size_bytes = os.path.getsize(file_path)
    file_size = float(file_size_bytes) / (1024 * 1024)  # Convert bytes to megabytes
    priority_level = "normal"

    # create JSON object with the file information

    file_info = {
        "file_id": file_id,
        "file_name": file_name,
        "file_size": file_size,
        "file_path": file_path,
        "priority_level": priority_level,
        "CID": cid_for_file_content,
    }
    file_info_list.append(file_info)
    file_info_json_str = json.dumps(file_info)

    try:
        # Run the IPFS command-line interface to add the JSON data
        completed_process = subprocess.run(["ipfs", "add", "-Q"], input=file_info_json_str, capture_output=True, text=True, check=True)

        # Get the CID (content identifier) from the command output
        cid_for_file_info = completed_process.stdout.strip()
        list_cid_for_file_info.append(cid_for_file_info)

        return cid_for_file_info
    except subprocess.CalledProcessError as e:
        print("Failed to add JSON to IPFS:", e)
        return None



def ipfs_add(file_path):
    try:
        # Run the IPFS command-line interface to add the file
        completed_process = subprocess.run(["ipfs", "add", "-Q", file_path], capture_output=True, text=True, check=True)

        # Get the CID (content identifier) from the command output
        file_cid = completed_process.stdout.strip()
        return file_cid
    except subprocess.CalledProcessError as e:
        print("Failed to add file to IPFS:", e)
        return None

def upload_information_of_file_to_ipfs(file_path):
    info = get_info_of_file(file_path, priority="normal")
    json_str = json.dumps(info)
    try:
        # Run the IPFS command-line interface to add the JSON data
        completed_process = subprocess.run(["ipfs", "add", "-Q"], input=json_str, capture_output=True, text=True, check=True)

        # Get the CID (content identifier) from the command output
        file_info_cid = completed_process.stdout.strip()
        return file_info_cid
    except subprocess.CalledProcessError as e:
        print("Failed to add JSON to IPFS:", e)
        return None

def get_file_sizes(file_info_list):
    file_sizes = []  # Initialize an empty list to store file sizes

    for file_info in file_info_list:
        file_size = file_info["file_size"]
        file_sizes.append(file_size)

    return file_sizes

def remove_cid_from_ipfs(cid):
    cid_string = str(cid)
    try:
        subprocess.run(["ipfs", "pin", "rm", cid_string], check=True)
        print(f"Removed CID {cid_string} from IPFS")
    except subprocess.CalledProcessError as e:
        print(f"Failed to remove CID {cid_string} from IPFS:", e)


