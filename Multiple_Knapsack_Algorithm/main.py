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
    # Same implementation as before, but include a list of priorities for each file

    for i in range(1, num_files + 1):
        file_size = files[i - 1]
        file_priority = priorities[i - 1]
        for j in range(1, num_devices + 1):
            device_capacity = devices[j - 1]
            if file_size <= device_capacity and dp[i - 1][j - 1] + file_priority > dp[i - 1][j]:
                dp[i][j] = dp[i - 1][j - 1] + file_priority
            else:
                dp[i][j] = dp[i - 1][j]

    # Rest of the code remains the same

# Example usage:
files = [5, 3, 7, 2, 4]
devices = [10, 8, 12]
priorities = [3, 2, 5, 1, 4]

total_storage, allocation_strategy = multiple_knapsack_with_priority(files, devices, priorities)
print("Optimal Total Storage with Priority:", total_storage)
print("Optimal Allocation Strategy (file index, device index):", allocation_strategy)


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

if __name__ == "__main__":
    main()
