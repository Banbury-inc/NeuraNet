devices = [
    {'device_name': 'michael-desktop', 'predicted_upload_speed': 7.753007, 'predicted_download_speed': 100.29564, 'predicted_gpu_usage': 9.700779, 'predicted_cpu_usage': 4.31928, 'predicted_ram_usage': 8.9832945},
    {'device_name': 'MichaelMills.local', 'predicted_upload_speed': 4.7662635, 'predicted_download_speed': 60.13842, 'predicted_gpu_usage': 59.375694, 'predicted_cpu_usage': 70.45171, 'predicted_ram_usage': 75.81698},
    {'device_name': 'michael-ubuntu', 'predicted_upload_speed': 22.379042, 'predicted_download_speed': 173.04262, 'predicted_gpu_usage': 24.893677, 'predicted_cpu_usage': 21.230713, 'predicted_ram_usage': 34.57914}
]

# Define the maximum and minimum for normalization from observed or expected ranges
max_upload_speed = max(device['predicted_upload_speed'] for device in devices)
min_upload_speed = min(device['predicted_upload_speed'] for device in devices)
max_download_speed = max(device['predicted_download_speed'] for device in devices)
min_download_speed = min(device['predicted_download_speed'] for device in devices)
max_gpu_usage = max(device['predicted_gpu_usage'] for device in devices)
min_gpu_usage = min(device['predicted_gpu_usage'] for device in devices)
max_cpu_usage = max(device['predicted_cpu_usage'] for device in devices)
min_cpu_usage = min(device['predicted_cpu_usage'] for device in devices)
max_ram_usage = max(device['predicted_ram_usage'] for device in devices)
min_ram_usage = min(device['predicted_ram_usage'] for device in devices)

# Calculate scores for each device
for device in devices:
    normalized_upload_speed = (device['predicted_upload_speed'] - min_upload_speed) / (max_upload_speed - min_upload_speed) * 100
    normalized_download_speed = (device['predicted_download_speed'] - min_download_speed) / (max_download_speed - min_download_speed) * 100
    normalized_gpu_usage = (1 - (device['predicted_gpu_usage'] - min_gpu_usage) / (max_gpu_usage - min_gpu_usage)) * 100
    normalized_cpu_usage = (1 - (device['predicted_cpu_usage'] - min_cpu_usage) / (max_cpu_usage - min_cpu_usage)) * 100
    normalized_ram_usage = (1 - (device['predicted_ram_usage'] - min_ram_usage) / (max_ram_usage - min_ram_usage)) * 100

    # Compute weighted score
    device['score'] = (
        0.3 * normalized_upload_speed +
        0.3 * normalized_download_speed +
        0.1 * normalized_gpu_usage +
        0.2 * normalized_cpu_usage +
        0.1 * normalized_ram_usage
    )

# Output the scores
for device in devices:
    print(f"Device: {device['device_name']}, Score: {device['score']:.2f}")

