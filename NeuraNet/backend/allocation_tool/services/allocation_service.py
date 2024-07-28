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

    def blocks(self, devices, total_num_blocks, model_size_in_billion_parameters):
        # Determine the amount of blocks that each device is capable of running
        # 0.7 GB per 1 billion parameters for model in 4-bit precision

        # Sort devices by score (descending)
        devices.sort(key=lambda x: x['score'], reverse=True)

        # Todo: in database, search through blocks and what devices they are allocated to
        # Todo: in database, assign priority rating based on what blocks are covered and which ones aren't
        # Todo: sort blocks by priority rating

        needed_ram_to_run_model = model_size_in_billion_parameters * 0.7
        amount_of_ram_per_block = needed_ram_to_run_model / total_num_blocks

        block_allocations = {device['device_name']: [] for device in devices}
        initial_total_num_blocks = total_num_blocks

        print(f"Needed RAM to run model: {needed_ram_to_run_model:.2f} GB")
        print(f"Amount of RAM per block: {amount_of_ram_per_block:.2f} GB")
        print("Initial total number of blocks: ", initial_total_num_blocks)

        for device in devices:
            total_ram_bytes = device['ram_total'][0]
            total_ram_gb = total_ram_bytes / (1024 ** 3)
            device_max_blocks = int(total_ram_gb / amount_of_ram_per_block)
            device['max_blocks'] = min(device_max_blocks, total_num_blocks)

            print(f"Device: {device['device_name']}, RAM: {total_ram_gb:.2f} GB, Max Blocks: {device['max_blocks']}")

        block_index = 0
        while block_index < total_num_blocks:
            allocated = False
            for device in devices:
                if len(block_allocations[device['device_name']]) < device['max_blocks']:
                    block_allocations[device['device_name']].append(block_index)
                    block_index += 1
                    allocated = True
                    if block_index >= total_num_blocks:
                        break
            if not allocated:
                break  # No more capacity to allocate blocks

        is_fully_allocated = (block_index >= total_num_blocks)


        blocks_allocated = block_index
        blocks_left_over = total_num_blocks - blocks_allocated

        print("Blocks allocated: ", blocks_allocated)
        print("Blocks left over: ", blocks_left_over)

        if not is_fully_allocated:
            print("Not enough devices to allocate all blocks")

        return block_allocations, is_fully_allocated


