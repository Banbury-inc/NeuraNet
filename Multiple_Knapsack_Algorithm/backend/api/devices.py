import paramiko

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

# Example usage:
hostname = "your_remote_device_hostname_or_ip"
username = "your_username"
password = "your_password"

device_list = []
device_name, storage_info = get_remote_device_info(hostname, username, password)
add_device_info_to_list(device_list, device_name, storage_info)

# You can now access the device information in the 'device_list' variable.
