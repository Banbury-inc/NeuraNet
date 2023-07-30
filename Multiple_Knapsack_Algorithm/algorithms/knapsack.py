def multiple_knapsack(files, devices):
    # Simplified implementation of the knapsack algorithm
    # Placeholder for the actual algorithm logic
    total_storage = sum(device["storage_capacity"] for device in devices)
    allocation_strategy = [(file["name"], devices[0]["name"]) for file in files]

    return total_storage, allocation_strategy
