class ScoringService():
    def __init__(self):
        pass

    def devices(self, performance_data):
        # Define the maximum and minimum for normalization from observed or expected ranges
        max_upload_speed = max(device.get('predicted_upload_speed', 0) for device in performance_data)
        min_upload_speed = min(device.get('predicted_upload_speed', 0) for device in performance_data)
        max_download_speed = max(device.get('predicted_download_speed', 0) for device in performance_data)
        min_download_speed = min(device.get('predicted_download_speed', 0) for device in performance_data)
        max_gpu_usage = max(device.get('predicted_gpu_usage', 0) for device in performance_data)
        min_gpu_usage = min(device.get('predicted_gpu_usage', 0) for device in performance_data)
        max_cpu_usage = max(device.get('predicted_cpu_usage', 0) for device in performance_data)
        min_cpu_usage = min(device.get('predicted_cpu_usage', 0) for device in performance_data)
        max_ram_usage = max(device.get('predicted_ram_usage', 0) for device in performance_data)
        min_ram_usage = min(device.get('predicted_ram_usage', 0) for device in performance_data)

        # Calculate scores for each device
        for device in performance_data:
            normalized_upload_speed = (device.get('predicted_upload_speed', 0) - min_upload_speed) / (max_upload_speed - min_upload_speed) * 100 if max_upload_speed != min_upload_speed else 0
            normalized_download_speed = (device.get('predicted_download_speed', 0) - min_download_speed) / (max_download_speed - min_download_speed) * 100 if max_download_speed != min_download_speed else 0
            normalized_gpu_usage = (1 - (device.get('predicted_gpu_usage', 0) - min_gpu_usage) / (max_gpu_usage - min_gpu_usage)) * 100 if max_gpu_usage != min_gpu_usage else 0
            normalized_cpu_usage = (1 - (device.get('predicted_cpu_usage', 0) - min_cpu_usage) / (max_cpu_usage - min_cpu_usage)) * 100 if max_cpu_usage != min_cpu_usage else 0
            normalized_ram_usage = (1 - (device.get('predicted_ram_usage', 0) - min_ram_usage) / (max_ram_usage - min_ram_usage)) * 100 if max_ram_usage != min_ram_usage else 0

            # Compute weighted score
            device['score'] = (
                0.3 * normalized_upload_speed +
                0.3 * normalized_download_speed +
                0.1 * normalized_gpu_usage +
                0.2 * normalized_cpu_usage +
                0.1 * normalized_ram_usage
            )

        scored_devices = performance_data
        return scored_devices
