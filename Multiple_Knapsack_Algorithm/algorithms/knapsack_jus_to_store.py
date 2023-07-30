# Optimlal Total Storage -- the maximum total size of files that can be shared across all the 
# devices without exceeding any device's storage capacity. 

def multiple_knapsack(files, devices):
    num_files = len(files)
    num_devices = len(devices)

    # Create a 2D array to store the intermediate results of subproblems
    dp = [[0 for _ in range(num_devices + 1)] for _ in range(num_files + 1)]

    # Dynamic programming computation
    for i in range(1, num_files + 1):
        file_size = files[i - 1]
        for j in range(1, num_devices + 1):
            device_capacity = devices[j - 1]
            if file_size <= device_capacity:
                dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - 1] + file_size)
            else:
                dp[i][j] = dp[i - 1][j]

    # Backtracking to find the optimal allocation
    optimal_allocation = []
    i, j = num_files, num_devices
    while i > 0 and j > 0:
        if dp[i][j] != dp[i - 1][j]:
            optimal_allocation.append((i - 1, j - 1))  # (file index, device index)
            i -= 1
            j -= 1
        else:
            i -= 1

    # Optimal total storage and allocation strategy
    total_storage = dp[num_files][num_devices]
    return total_storage, optimal_allocation

def multiple_knapsack_with_priority(files, devices, priorities):
    num_files = len(files)
    num_devices = len(devices)

    # Create a 2D array to store the intermediate results of subproblems
    dp = [[0 for _ in range(num_devices + 1)] for _ in range(num_files + 1)]

    # Dynamic programming computation
    for i in range(1, num_files + 1):
        file_size = files[i - 1]
        file_priority = priorities[i - 1]
        for j in range(1, num_devices + 1):
            device_capacity = devices[j - 1]
            if file_size <= device_capacity and dp[i - 1][j - 1] + file_priority > dp[i - 1][j]:
                dp[i][j] = dp[i - 1][j - 1] + file_priority
            else:
                dp[i][j] = dp[i - 1][j]

    # Backtracking to find the optimal allocation with priorities
    optimal_allocation = []
    i, j = num_files, num_devices
    while i > 0 and j > 0:
        file_size = files[i - 1]
        file_priority = priorities[i - 1]
        if file_size <= devices[j - 1] and dp[i][j] != dp[i - 1][j]:
            optimal_allocation.append((i - 1, j - 1))  # (file index, device index)
            i -= 1
            j -= 1
        else:
            i -= 1

    # Optimal total storage with priority-based allocation and the allocation strategy
    total_storage = dp[num_files][num_devices]
    return total_storage, optimal_allocation

# Example usage:
files = [5, 3, 7, 2, 4]  # Sizes of the files
devices = [10, 8, 12]   # Capacities of the devices
priorities = [3, 2, 5, 1, 4]  # Priorities of the files

total_storage, allocation_strategy = multiple_knapsack_with_priority(files, devices, priorities)
print("Optimal Total Storage with Priority:", total_storage)
print("Optimal Allocation Strategy (file index, device index):", allocation_strategy)


def multiple_knapsack_with_duplication(files, devices):
    num_files = len(files)
    num_devices = len(devices)

    # Create a 2D array to store the intermediate results of subproblems
    dp = [[0 for _ in range(num_devices + 1)] for _ in range(num_files + 1)]

    # 2D array to track the count of files allocated to each device
    file_counts = [[0 for _ in range(num_devices)] for _ in range(num_files + 1)]

    # Dynamic programming computation
    for i in range(1, num_files + 1):
        file_size = files[i - 1]
        for j in range(1, num_devices + 1):
            device_capacity = devices[j - 1]
            dp[i][j] = dp[i - 1][j]  # Without selecting the current file
            for k in range(1, min(device_capacity // file_size, i) + 1):
                if dp[i - k][j - 1] + k * file_size > dp[i][j]:
                    dp[i][j] = dp[i - k][j - 1] + k * file_size
                    file_counts[i][j - 1] = k

    # Backtracking to find the optimal allocation with file duplication
    optimal_allocation = []
    i, j = num_files, num_devices
    while i > 0 and j > 0:
        k = file_counts[i][j - 1]
        for _ in range(k):
            optimal_allocation.append((i - 1, j - 1))  # (file index, device index)
        i -= k
        j -= 1

    # Optimal total storage with file duplication and the allocation strategy
    total_storage = dp[num_files][num_devices]
    return total_storage, optimal_allocation

# Example usage:
files = [5, 3, 7, 2, 4]  # Sizes of the files
devices = [10, 8, 12]   # Capacities of the devices

total_storage, allocation_strategy = multiple_knapsack_with_duplication(files, devices)
print("Optimal Total Storage with File Duplication:", total_storage)
print("Optimal Allocation Strategy (file index, device index):", allocation_strategy)

def multiple_knapsack_with_file_sharing(files, devices, parts):
    num_files = len(files)
    num_devices = len(devices)

    # Create a 3D array to store the intermediate results of subproblems
    dp = [[[0 for _ in range(num_devices + 1)] for _ in range(parts + 1)] for _ in range(num_files + 1)]

    # Dynamic programming computation
    for i in range(1, num_files + 1):
        file_size = files[i - 1]
        for p in range(1, parts + 1):
            for j in range(1, num_devices + 1):
                device_capacity = devices[j - 1]
                dp[i][p][j] = dp[i - 1][p][j]  # Without selecting the current file
                for k in range(1, min(device_capacity // (file_size // p), i) + 1):
                    if dp[i - k][p - 1][j - 1] + (k * (file_size // p)) > dp[i][p][j]:
                        dp[i][p][j] = dp[i - k][p - 1][j - 1] + (k * (file_size // p))

    # Backtracking to find the optimal allocation with limited file sharing
    optimal_allocation = []
    i, p, j = num_files, parts, num_devices
    while i > 0 and p > 0 and j > 0:
        k = 0
        while k < parts and dp[i][p][j] == dp[i][p][j - 1]:
            k += 1
        for _ in range(k):
            optimal_allocation.append((i - 1, p - 1, j - 1))  # (file index, part, device index)
        i -= k
        p -= 1
        j -= 1

    # Optimal total storage with limited file sharing and the allocation strategy
    total_storage = dp[num_files][parts][num_devices]
    return total_storage, optimal_allocation

# Example usage:
files = [10, 15, 8, 12]  # Sizes of the files
devices = [20, 25, 30]   # Capacities of the devices
parts = 2  # Number of parts to split each file

total_storage, allocation_strategy = multiple_knapsack_with_file_sharing(files, devices, parts)
print("Optimal Total Storage with Limited File Sharing:", total_storage)
print("Optimal Allocation Strategy (file index, part, device index):", allocation_strategy)

# Main function
def main():
    # Example input data
    files = [50, 35, 7, 200, 4]  # Sizes of the files
    devices = [1000, 500, 250]   # Capacities of the devices in GB

    # Solve the Multiple Knapsack Problem
    total_storage, allocation_strategy = multiple_knapsack(files, devices)

    # Display the results

    # Optimlal Total Storage -- the maximum total size of files that can be shared across all the 
    # devices without exceeding any device's storage capacity. 
    print("Optimal Total Storage:", total_storage)
    
    # Optimal Allocation Strategy -- the specific way of allocating the files among the devices
    # to achieve the maximum total storage without violating any device's capacity constraint 
    print("Optimal Allocation Strategy (file index, device index):", allocation_strategy)


    # call multiple knapsack with file sharing
    total_storage, allocation_strategy = multiple_knapsack_with_file_sharing(files, devices, parts)



if __name__ == "__main__":
    main()
