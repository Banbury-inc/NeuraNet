# main.py
import tkinter as tk
from backend.utils.choose_file import choose_file
from backend.api import scan_files
from backend.api import devices
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
        print("6. Quit")

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
            device_storage_list = [device_info["storage_space"] for device_info in device_list]
            print(file_size_list)
            print(device_storage_list)
            # parts = 2 # number of parts to split the file
            total_storage, allocation_strategy = knapsack_just_to_store.multiple_knapsack(file_size_list, device_storage_list)
            print("Optimal Total Storage:", total_storage)
            print("Optimal Allocation Strategy (file index, device index):", allocation_strategy)

#            total_storage, allocation_strategy = knapsack_just_to_store.multiple_knapsack_with_duplication(file_size_list, device_list)
#            print("Optimal Total Storage with Duplication:", total_storage)
#            print("Optimal Allocation Strategy (file index, device index):", allocation_strategy)
#            total_storage, allocation_strategy = knapsack_just_to_store.multiple_knapsack_with_file_sharing(file_size_list, device_list, parts)
#            print("Optimal Total Storage with file sharing:", total_storage)
#            print("Optimal Allocation Strategy (file index, device index):", allocation_strategy)

        # if the user wants to quit
        if user_input == "6":
            break

if __name__ == "__main__":
    main()
