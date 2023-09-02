# main.py
import tkinter as tk
from backend.utils.choose_file import choose_file
from backend.api import scan_files
from backend.api import devices
from backend.api import user_management
from algorithms import knapsack_just_to_store
from decentralized_storage import ipfs
import pprint
import getpass

def main():
    device_list = []
    file_info_list = []
    while True:
        # give a selection of options to chose from
        print("Welcome, what would you like to do today?")
        print("1. Scan a single folder")
        print("2. Connect a device")
        print("3. List devices")
        print("4. List scanned files")
        print("5. Calculate optimal allocation strategy")
        print("6. Calculate optimal allocation strategy with example devices/files")
        print("7. Signup with sample user data")
        print("8. Log in with sample user data")
        print("9. Sign up")
        print("10. Log in")
        print("11. Quit")

        # get the input from the user
        user_input = input("Please enter a number: ")

        # scan a single folder
        if user_input == "1":
            # get the path to the folder
            path = choose_file()  # Call the function to get the folder path

            if path:
                # scan the folder
                file_info_list = scan_files.scan_folder(path)
                print("Files found in the folder:")
                for file_info in file_info_list:
                    print(f"File Name: {file_info['file_name']}")
                    print(f"File Size (MB): {file_info['file_size']:.2f}")
                    print(f"File Path: {file_info['file_path']}")
                    print(f"Priority Level: {file_info['priority_level']}")
                    print()
                    print(f"CID: {file_info['CID']}")
            else:
                print("No folder selected.")
        # connect a device
        if user_input == "2":
            # Replace these with the actual credentials and remote device's hostname
            # Get user inputs or use default values
            remote_hostname = input("Enter the remote hostname (default: localhost): ") or "localhost"
            remote_username = input("Enter your username: ")
            remote_password = getpass.getpass("Enter your password: ")
            device_name, storage_info = devices.get_remote_device_info(remote_hostname, remote_username, remote_password)
    
            if devices.add_device_info_to_list(device_list, device_name, storage_info):
                ipfs_client = devices.connect_device_to_ipfs()
                if ipfs_client:
                    print("Device Name:", device_name)
                    print("Available Storage Space: " + str(storage_info) + " GB")  # Convert storage_info to string                print(device_list)
            else:
                print("Failed to obtain remote device information.")
    

        # list devices
        if user_input == "3":
            pprint.pprint(device_list)
        # list the devices

        # list files
        if user_input == "4":
            # list the files
            pprint.pprint(file_info_list)

        # calculate optimal allocation strategy
        if user_input == "5":
            # extract just the file sizes from the file size list
            file_size_list = [file_info["file_size"] for file_info in file_info_list]
            # extract just the total storage from the device list
            device_storage_list = [round(device_info["storage_space"], 2) for device_info in device_list]

            print(file_size_list)
            print(device_storage_list)
            # parts = 2 # number of parts to split the file
            print("Allocate Files:")
            total_storage_used, allocation, files_not_allocated = knapsack_just_to_store.allocate_files(file_size_list, device_storage_list)
            for i, device_storage in enumerate(total_storage_used):
                print(f"Device {i + 1} - Total Storage Used: {device_storage} GB")
                print(f"Files Allocated: {', '.join(map(str, allocation[i]))}")
                print()
            print("Files Not Allocated:", files_not_allocated)
            print()

        # calculate optimal allocation strategy with example devices and files
        if user_input == "6":
            # extract just the file sizes from the file size list
#            file_size_list = [50, 35, 7, 200, 4, 20, 11, 1, 5, 90, 100, 100, 50]
            file_size_list =  [50, 35, 7, 200, 4]  
            # extract just the total storage from the device list
 #           device_storage_list = [250, 200, 250]
            device_storage_list = [1000, 500, 250]
            priority = [3, 2, 1, 2, 3] # priority of the file. Higher the value the higher the priority. 
            duplication_factor = 2 # how many copies of each file should be allocated
            sharing_factor = 3 # how many devices should share the allocation of a file
            print()
            print("-----------------------------------------------------------------")
            print("Allocate Files:")
            print()
            total_storage_used, allocation, files_not_allocated = knapsack_just_to_store.allocate_files(file_size_list, device_storage_list)
            for i, device_storage in enumerate(total_storage_used):
                print(f"Device {i + 1} - Total Storage Used: {device_storage} GB")
                print(f"Files Allocated: {', '.join(map(str, allocation[i]))}")
                print()
            print("Files Not Allocated:", files_not_allocated)
            print()
            print("-----------------------------------------------------------------")
            print("Allocate Files with priority:")
            print()
            total_storage_used, allocation, files_not_allocated = knapsack_just_to_store.allocate_files_with_priority(file_size_list, device_storage_list, priority)
            for i, device_storage in enumerate(total_storage_used):
                print(f"Device {i + 1} - Total Storage Used: {device_storage} GB")
                print(f"Files Allocated: {', '.join(map(str, allocation[i]))}")
                print()
     
            print("Files Not Allocated:", files_not_allocated)
            print()
            print("-----------------------------------------------------------------")
            print("Allocate Files with duplication:")
            print()
            total_storage_used, allocation, files_not_allocated = knapsack_just_to_store.allocate_files_with_duplication(file_size_list, device_storage_list, duplication_factor)
            for i, device_storage in enumerate(total_storage_used):
                print(f"Device {i + 1} - Total Storage Used: {device_storage} GB")
                print(f"Files Allocated: {', '.join(map(str, allocation[i]))}")
                print()
            

            print("Files Not Allocated:", files_not_allocated)
            print()
            print("-----------------------------------------------------------------")
            print("Allocate Files with file sharing:")
            print()
            total_storage_used, allocation, files_not_allocated = knapsack_just_to_store.allocate_files_with_file_sharing(file_size_list, device_storage_list, sharing_factor)
            for i, device_storage in enumerate(total_storage_used):
                print(f"Device {i + 1} - Total Storage Used: {device_storage} GB")
                print(f"Files Allocated: {', '.join(map(str, allocation[i]))}")
                print()
     

            print("Files Not Allocated:", files_not_allocated)
            print()
            print("-----------------------------------------------------------------")
            print("Allocate Files with priority, duplication, and file sharing:")
            print()
            total_storage_used, allocation, files_not_allocated = knapsack_just_to_store.allocate_files_with_priority_duplication_file_sharing(file_size_list, device_storage_list, priority, duplication_factor, sharing_factor)
            for i, device_storage in enumerate(total_storage_used):
                print(f"Device {i + 1} - Total Storage Used: {device_storage} GB")
                print(f"Files Allocated: {', '.join(map(str, allocation[i]))}")
                print()
     

            print("Files Not Allocated:", files_not_allocated)
            print()
        # exit
        if user_input == "7":
            username = "john_doe"
            password = "secretpassword"
            first_name = "Michael" 
            last_name = "Mills"
            user_cid = user_management.register_user(username, password, first_name, last_name)
            print("User registered with CID:", user_cid)



        if user_input == "8":
            username = "john_doe"
            password = "secretpassword"
            user_id = user_management.authenticate_user(username, password)

            if user_id:
                print("User authenticated. User ID:", user_id)
            else:
                print("Authentication failed. Invalid username or password.")
        if user_input == "9":
            username = input("Enter a username: ")
            password = getpass.getpass("Enter your password: ")
            first_name = input("Enter a first name: ")
            last_name = input("Enter a last name: ")
            user_cid = user_management.register_user(username, password, first_name, last_name)
            print("User registered with CID:", user_cid)



        if user_input == "10":
            username = input("Enter a username: ")
            password = getpass.getpass("Enter your password: ")
            user_id = user_management.authenticate_user(username, password)

            if user_id:
                print("Welcome " + user_id[2] + " " + user_id[3])
            else:
                print("Authentication failed. Invalid username or password.")



        if user_input == "11":
            break



if __name__ == "__main__":
    main()
