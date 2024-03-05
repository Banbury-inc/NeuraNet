import psutil
import GPUtil
import subprocess
import re

def get_wifi_speed():
    command = "speedtest"
    network_speed_result = subprocess.run(command, shell=True, capture_output=True, check=True, text=True)
    # Use regular expressions to extract the Wi-Fi speed
    download_speed_pattern = r"Download:\s+(\d+(\.\d+)?)\s[MG]?bit/s"
    match = re.search(download_speed_pattern, network_speed_result.stdout)
    if match:
        download_speed_value = match.group(1)
        download_network_speed = download_speed_value
    else:
        download_network_speed = 0

    upload_speed_pattern = r"Upload:\s+(\d+(\.\d+)?)\s[MG]?bit/s"
    match = re.search(upload_speed_pattern, network_speed_result.stdout)
    if match:
        upload_speed_value = match.group(1)
        upload_network_speed = upload_speed_value
    else:
        upload_network_speed = 0
    return upload_network_speed, download_network_speed

wifi_speed = get_wifi_speed()
print(wifi_speed)





