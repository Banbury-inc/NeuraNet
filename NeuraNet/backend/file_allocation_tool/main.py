from api.get_data import Get
from services.prediction_service import PredictionService
from services.scoring_service import ScoringService
from services.allocation_service import AllocationService
def main():
    get = Get()
    predict = PredictionService()
    devices = get.devices()
    # print(devices)

    for device in devices:
        device['capacity'] = device.get('storage_capacity_GB', 0)  # Default to 0 if not found


    performance_data = predict.performance_data(devices, show_graph=False)
    print(performance_data)

    score = ScoringService() 
    scored_devices = score.devices(performance_data)

    for device in scored_devices:
        print(f"Device: {device['device_name']}, Score: {device['score']:.2f}")

    allocate = AllocationService() 


    # files = [
    #     {"file_name": "File 1", "priority": "high", "size": 50},
    #     {"file_name": "File 2", "priority": "medium", "size": 200},
    #     {"file_name": "File 3", "priority": "high", "size": 150},
    #     {"file_name": "File 4", "priority": "low", "size": 100},
    #     {"file_name": "File 5", "priority": "high", "size": 300}
    # ]

    files = get.files()

    for device in scored_devices:
        # This assumes the original devices list and performance_data have matching order and contents
        original_device = next(d for d in devices if d['device_name'] == device['device_name'])
        device['capacity'] = original_device['capacity']  # Assign capacity from the original fetched data

    allocated_devices = allocate.devices(scored_devices, files)
    
    for device in allocated_devices:
        print(f"Device: {device['device_name']}, Stored Files: {device['files']}, Used Capacity: {device['used_capacity']}/{device['capacity']}")

    print("")
    allocated_devices_with_cap = allocate.devices_with_capacity_cap(scored_devices, files, .0005)
    for device in allocated_devices_with_cap:
        print(f"Device: {device['device_name']}, Stored Files: {device['files']}, Used Capacity: {device['used_capacity']}/{device['capacity']}")

if __name__ == "__main__":
    main()

