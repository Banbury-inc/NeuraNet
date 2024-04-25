# Example data
devices = [
    {"device_name": "Device A", "score": 90, "capacity": 500},
    {"device_name": "Device B", "score": 80, "capacity": 300},
    {"device_name": "Device C", "score": 70, "capacity": 450}
]


class AllocationService():
    def __init__(self):
        pass
    def bytes_to_gigabytes(self, bytes):
        return bytes / (1024 ** 3)  # Convert bytes to gigabytes

    def devices(self, devices, files):
        # Sort devices by score (descending)
        devices.sort(key=lambda x: x['score'], reverse=True)

        # Sort files by priority and size (descending)
        priority_map = {"high": 3, "medium": 2, "low": 1}
        files.sort(key=lambda x: (priority_map[x['priority']], -x['size']), reverse=True)

        # Allocate files to devices
        for device in devices:
            device['files'] = []
            device['used_capacity'] = 0  # Initialize used capacity in gigabytes

        for file in files:
            file_size_gb = self.bytes_to_gigabytes(file['size'])  # Convert file size to gigabytes
            for device in devices:
                if device['used_capacity'] + file_size_gb <= device['capacity']:
                    device['files'].append(file['file_name'])
                    device['used_capacity'] += file_size_gb
                    break

        return devices
    def devices_with_capacity_cap(self, devices, files, device_capcity_cap):
        # Sort devices by score (descending)
        devices.sort(key=lambda x: x['score'], reverse=True)

        # Sort files by priority and size (descending)
        priority_map = {"high": 3, "medium": 2, "low": 1}
        files.sort(key=lambda x: (priority_map[x['priority']], -x['size']), reverse=True)

        # Allocate files to devices
        for device in devices:
            device['capacity'] = device_capcity_cap
            device['files'] = []
            device['used_capacity'] = 0  # Initialize used capacity in gigabytes

        for file in files:
            file_size_gb = self.bytes_to_gigabytes(file['size'])  # Convert file size to gigabytes
            for device in devices:
                if device['used_capacity'] + file_size_gb <= device['capacity']:
                    device['files'].append(file['file_name'])
                    device['used_capacity'] += file_size_gb
                    break

        return devices

