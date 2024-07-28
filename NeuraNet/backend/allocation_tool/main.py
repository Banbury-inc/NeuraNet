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

    date = f'2024-05-5 19:25:50.473372'
    try:
        performance_data = predict.performance_data(devices, date, show_graph=False)
    except Exception as e:
        print(f"Error: {e}")
        return

    score = ScoringService() 
    scored_devices = score.devices(performance_data)
    print(scored_devices)
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

    allocated_devices = allocate.files(scored_devices, files)
    
    for device in allocated_devices:
        print(f"Device: {device['device_name']}, Stored Files: {device['files']}, Used Capacity: {device['used_capacity']}/{device['capacity']}")

    print("")
    allocated_devices_with_cap = allocate.files_with_capacity_cap(scored_devices, files, .0001)
    for device in allocated_devices_with_cap:
        print(f"Device: {device['device_name']}, Stored Files: {device['files']}, Used Capacity: {device['used_capacity']}/{device['capacity']}")

    allocated_blocks = allocate.blocks(scored_devices, total_num_blocks=32)
    for device in allocated_blocks:
        print(f"Device: {device['device_name']}, Blocks: {device['blocks']}")



if __name__ == "__main__":
    main()

