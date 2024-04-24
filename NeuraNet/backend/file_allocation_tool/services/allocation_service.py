# Example data
devices = [
    {"device_name": "Device A", "score": 90, "capacity": 500},
    {"device_name": "Device B", "score": 80, "capacity": 300},
    {"device_name": "Device C", "score": 70, "capacity": 450}
]

files = [
    {"file_name": "File 1", "priority": "high", "size": 50},
    {"file_name": "File 2", "priority": "medium", "size": 200},
    {"file_name": "File 3", "priority": "high", "size": 150},
    {"file_name": "File 4", "priority": "low", "size": 100},
    {"file_name": "File 5", "priority": "high", "size": 300}
]


class AllocationService():
    def __init__(self):
        pass
    def devices(self, devices, files):
        # Sort devices by score (descending)
        devices.sort(key=lambda x: x['score'], reverse=True)

        # Sort files by priority and size (descending)
        priority_map = {"high": 3, "medium": 2, "low": 1}
        files.sort(key=lambda x: (priority_map[x['priority']], x['size']), reverse=True)

        # Allocate files to devices
        for device in devices:
            device['files'] = []
            device['used_capacity'] = 0

        for file in files:
            for device in devices:
                if device['used_capacity'] + file['size'] <= device['capacity']:
                    device['files'].append(file['file_name'])
                    device['used_capacity'] += file['size']
                    break

        return devices


