import unittest
from algorithms import knapsack_just_to_store
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

if __name__ == '__main__':
    unittest.main()
