import os
import paramiko
import ipfshttpclient
import psutil
import subprocess

def get_remote_device_info(hostname, username, password):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the remote device
        ssh_client.connect(hostname, username=username, password=password)

        # Get the device name using the 'uname' command
        stdin, stdout, stderr = ssh_client.exec_command("uname -n")
        device_name = stdout.read().decode().strip()

        if not device_name:
            # If the 'uname -n' command fails, try the 'hostname' command instead
            stdin, stdout, stderr = ssh_client.exec_command("hostname")
            device_name = stdout.read().decode().strip()

        # Get storage space information using the 'df' command
        stdin, stdout, stderr = ssh_client.exec_command("df -h / | tail -1 | awk '{print $4}'")
        storage_info = stdout.read().decode().strip()

        if not storage_info:
            # If the 'df' command fails, try the Windows equivalent command using 'wmic'
            stdin, stdout, stderr = ssh_client.exec_command("wmic logicaldisk where DeviceID='C:' get FreeSpace")
            # get the free space value
            storage_info_bytes = stdout.read().decode().strip().split("\n")[1].strip()
            # Convert storage space from bytes to gigabytes
            # Convert storage space from bytes to gigabytes (float) and then round it to an integer
            storage_info = int(round(float(storage_info_bytes) / (1024 * 1024 * 1024), 0))
        # Close the SSH connection
        ssh_client.close()

        return device_name, storage_info
    except Exception as e:
        print(f"Error: {e}")
        return None, None

def add_device_info_to_list(device_list, device_name, storage_info):
    if device_name and storage_info:
        device_list.append({"device_name": device_name, "storage_space": storage_info})
        return True
    return False

def start_ipfs_daemon():
    try:

        # Start the IPFS daemon
        subprocess.Popen(['ipfs', 'daemon'])
        print("IPFS daemon started.")
        return True
    except subprocess.CalledProcessError as e:
        print("Failed to start IPFS daemon:", e)
        return False
    
def initialize_IPFS():
    try:

        # Start the IPFS daemon
        subprocess.Popen(['ipfs', 'init'])
        print("IPFS daemon initialized.")
        return True
    except subprocess.CalledProcessError as e:
        print("Failed to start IPFS daemon:", e)
        return False

def connect_device_to_ipfs():
    try:
        # Execute 'ipfs id' command and capture the output
        completed_process = subprocess.run(['ipfs', 'id'], capture_output=True, text=True)
        output = completed_process.stdout

        # Check if the 'Addresses' field is null
        if '"Addresses": null' in output:
            print("IPFS node has null Addresses. Starting IPFS daemon...")
            start_ipfs_daemon()
            return True
        else:
            print("IPFS node is already running.")
            return False
    except subprocess.CalledProcessError as e:
        print("Failed to check IPFS ID:", e)
        return False
 
def main():
    connect_device_to_ipfs()
    print("Connection to device is complete")
if __name__ == "__main__":
    main()


