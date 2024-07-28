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

    def files(self, devices, files):
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
    def files_with_capacity_cap(self, devices, files, device_capcity_cap):
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
    def blocks(self, devices, total_num_blocks):
        
        # Determine the amount of blocks that each device is capable of running

        # 0.7 gb per 1 billion parameters for model in 4 bit precision

        model_size_in_billion_parameters = 8

        for device in devices:
            total_ram_bytes = device['ram_total']
            total_ram_gb = total_ram_bytes / (1024 ** 3)
            print(f"Device: {device['device_name']}, RAM: {total_ram_gb:.2f} GB")
            needed_ram_to_run_model = total_ram_gb / (model_size_in_billion_parameters * 0.7)
            print(f"Needed RAM to run model: {needed_ram_to_run_model:.2f} GB")

            # Determine the number of blocks based on needed RAM vs total RAM
            device_max_blocks = int(total_ram_gb / needed_ram_to_run_model)
            print("Device max blocks: ", device_max_blocks)

            # If max blocks is greater than total_num_blocks, set max blocks to total_num_blocks
            if device_max_blocks > total_num_blocks:
                device_max_blocks = total_num_blocks
                device['max_blocks'] = device_max_blocks
            print("Device max blocks after adjustment: ", device_max_blocks)
        
        block_allocations = {device['device_name']: 0 for device in devices}
        
        # Allocate blocks to devices based on their score
        for device in devices:
            while total_num_blocks > 0 and block_allocations[device['device_name']] < device['max_blocks']:
                block_allocations[device['device_name']] += 1
                total_num_blocks -= 1
                if total_num_blocks == 0:
                    break
        
        return block_allocations
