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

        # Get storage space information using the 'df' command
        stdin, stdout, stderr = ssh_client.exec_command("df -h / | tail -1 | awk '{print $4}'")
        storage_info = stdout.read().decode()

        # Close the SSH connection
        ssh_client.close()

        return device_name, storage_info
    except Exception as e:
        print(f"Error: {e}")
        return None, None

def add_device_info_to_list(device_list, device_name, storage_info):
    if device_name and storage_info:
        device_list.append({"device_name": device_name, "storage_info": storage_info})
        return True
    return False