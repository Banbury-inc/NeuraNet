# main.py
from backend.api import scan_files
from backend.api import devices
from algorithms import knapsack_just_to_store

def main():
    device_list = []
    while True:
        # give a selection of options to chose from
        print("Welcome, what would you like to do today?")
        print("1. Scan a single folder")
        print("2. Connect a device")
        print("3. List devices")
        print("4. List files")
        print("5. Calculate optimal allocation strategy")
        print("6. Quit")

        # get the input from the user
        user_input = input("Please enter a number: ")

        # if the user wants to scan a single folder
        if user_input == "1":
            # get the path to the folder
            path = input("Please enter the path to the folder: ")
            # scan the folder
            scan_files.scan_folder(path)

        # if the user wants to connect a device
        if user_input == "2":
            # Replace these with the actual credentials and remote device's hostname
            # Get user inputs or use default values
            remote_hostname = input("Enter the remote hostname (default: localhost): ") or "localhost"
            remote_username = input("Enter your username: ")
            remote_password = input("Enter your password: ")
            device_name, storage_info = devices.get_remote_device_info(remote_hostname, remote_username, remote_password)
    
            if devices.add_device_info_to_list(device_list, device_name, storage_info):
                print("Device Name:", device_name)
                print("Available Storage Space:", storage_info)
                print(device_list)
            else:
                print("Failed to obtain remote device information.")
    
        # connect the device

        # if the user wants to list devices
        if user_input == "3":
            print("This is not implemented yet")
        # list the devices

        # if the user wants to list files
        if user_input == "4":
            # list the files
            print("This is not implemented yet")

        # If the user wants to calculate optimal allocation strategy
        if user_input == "5":
            # list the files
            print("This is not implemented yet")
            # For scanning a single folder
            file_info_list = scan_files.file_info_list
            print(file_info_list)
            # get just a list of the file sizes in file_info_list
            file_size_list = scan_files.get_file_sizes(file_info_list)
            print(file_size_list)
            # call the algorithm 
            devices_list = scan_files.get_devices()
            parts = 2 # number of parts to split the file
            total_storage, allocation_strategy = knapsack_just_to_store.multiple_knapsack(file_size_list, devices)
            print("Optimal Total Storage:", total_storage)
            print("Optimal Allocation Strategy (file index, device index):", allocation_strategy)
            total_storage, allocation_strategy = knapsack_just_to_store.multiple_knapsack_with_duplication(file_size_list, devices)
            print("Optimal Total Storage with Duplication:", total_storage)
            print("Optimal Allocation Strategy (file index, device index):", allocation_strategy)
            total_storage, allocation_strategy = knapsack_just_to_store.multiple_knapsack_with_file_sharing(file_size_list, devices, parts)
            print("Optimal Total Storage with file sharing:", total_storage)
            print("Optimal Allocation Strategy (file index, device index):", allocation_strategy)

        # if the user wants to quit
        if user_input == "6":
            break

if __name__ == "__main__":
    main()
