import unittest
from algorithms import knapsack_just_to_store
import time
import matplotlib.pyplot as plt

# Import the allocation functions from your module
# from your_module import allocate_files, allocate_files_with_priority, ...

class TestAllocationFunctions(unittest.TestCase):

    def test_allocate_files(self):
        files = [50, 35, 7, 200, 4]
        devices = [1000, 500, 250]
        total_storage_used, allocation, files_not_allocated = knapsack_just_to_store.allocate_files(files, devices)
        
        self.assertEqual(sum(total_storage_used), sum(files), "Total storage used should be equal to the sum of file sizes")
        self.assertEqual(sum(total_storage_used), sum([sum(device) for device in allocation]), "Total storage used should be equal to the sum of allocated file sizes")
        self.assertEqual(len(files_not_allocated), 0, "No files should be unallocated")

    def test_allocate_files_with_priority(self):
        files = [50, 35, 7, 200, 4]
        devices = [1000, 500, 250]
        priority = [3, 2, 1, 4, 5]
        total_storage_used, allocation, files_not_allocated = knapsack_just_to_store.allocate_files_with_priority(files, devices, priority)
        
        self.assertEqual(sum(total_storage_used), sum(files), "Total storage used should be equal to the sum of file sizes")
        self.assertEqual(sum(total_storage_used), sum([sum(device) for device in allocation]), "Total storage used should be equal to the sum of allocated file sizes")
        self.assertEqual(len(files_not_allocated), 0, "No files should be unallocated")

    def test_allocate_files_with_not_enough_storage(self):
        files = [50, 35, 7, 200, 4, 300, 300, 500, 200, 100, 500, 35]
        devices = [1000, 500, 250]
        duplication_factor = 2
        total_storage_used, allocation, files_not_allocated = knapsack_just_to_store.allocate_files(files, devices)
        
        self.assertEqual(len(files_not_allocated), 6, "There should be unallocated files")
    def test_allocate_files_with_file_sharing_with_not_enough_storage(self):
        files = [50, 35, 7, 200, 4, 300, 300, 500, 200, 100, 500, 35]
        devices = [1000, 500, 250]
        duplication_factor = 2
        total_storage_used, allocation, files_not_allocated = knapsack_just_to_store.allocate_files_with_file_sharing(files, devices, duplication_factor)
        
        self.assertEqual(len(files_not_allocated), 1, "There should be unallocated files")

    def test_allocate_files_with_duplication_with_not_enough_storage(self):
        files = [50, 35, 7, 200, 4, 300, 300, 500, 200, 100, 500, 35]
        devices = [1000, 500, 250]
        duplication_factor = 2
        total_storage_used, allocation, files_not_allocated = knapsack_just_to_store.allocate_files_with_duplication(files, devices, duplication_factor)
        
        self.assertEqual(len(files_not_allocated), 1, "There should be unallocated files")


    def test_allocate_files_with_file_sharing(self):
        files = [50, 35, 7, 200, 4]
        devices = [1000, 500, 250]
        sharing_factor = 3
        total_storage_used, allocation, files_not_allocated = knapsack_just_to_store.allocate_files_with_file_sharing(files, devices, sharing_factor)
        
        self.assertEqual(sum(total_storage_used), sum([sum(device) for device in allocation]), "Total storage used should be equal to the sum of allocated file sizes")
        self.assertEqual(len(files_not_allocated), 0, "No files should be unallocated")

    def test_allocate_files_with_priority_duplication_file_sharing(self):
        files = [50, 35, 7, 200, 4]
        devices = [1000, 500, 250]
        priority = [3, 2, 1, 4, 5]
        duplication_factor = 2
        sharing_factor = 3
        total_storage_used, allocation, files_not_allocated = knapsack_just_to_store.allocate_files_with_priority_duplication_file_sharing(files, devices, priority, duplication_factor, sharing_factor)
        
        self.assertEqual(len(files_not_allocated), 0, "No files should be unallocated")
    
    # Begin time complexity analysis


    def time_complexity():
        # Define the input sizes you want to test
        file_sizes = [10, 50, 100, 500]  # Example input sizes
        device_counts = [10, 50, 100, 500]  # Example input sizes

        execution_times = []

        for files in file_sizes:
            for devices in device_counts:
                start_time = time.time()
                # Call your algorithms here with the given input sizes
                result = knapsack_just_to_store.allocate_files(files, devices)
                # result = allocate_files_with_priority(files, devices, priority)
                # ...
                end_time = time.time()
                execution_time = end_time - start_time
                execution_times.append((files, devices, execution_time))

        # Separate execution times for plotting
        file_sizes = [item[0] for item in execution_times]
        device_counts = [item[1] for item in execution_times]
        times = [item[2] for item in execution_times]

        # Create a scatter plot
        plt.scatter(device_counts, times)
        plt.xlabel("Number of Devices")
        plt.ylabel("Execution Time")
        plt.title("Execution Time vs. Number of Devices")
        plt.show()
if __name__ == '__main__':
    unittest.main()
