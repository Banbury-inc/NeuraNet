from api.get_data import Get
from services.prediction_service import PredictionService
from services.scoring_service import ScoringService

def main():
    get = Get()
    predict = PredictionService()
    devices = get.devices()
    print(devices)
    performance_data = predict.performance_data(devices, show_graph=False)
    print(performance_data)

    score = ScoringService() 
    scored_devices = score.devices(performance_data)

    for device in scored_devices:
        print(f"Device: {device['device_name']}, Score: {device['score']:.2f}")

if __name__ == "__main__":
    main()
