import os
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pymongo import MongoClient
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from dotenv import load_dotenv

def create_dataset(X, y, time_steps=1):
    Xs, ys = [], []
    for i in range(len(X) - time_steps):
        v = X.iloc[i:(i + time_steps)].values
        Xs.append(v)
        ys.append(y.iloc[i + time_steps])
    return np.array(Xs), np.array(ys)

def build_and_train_model(X_train, y_train, time_steps, features):
    model = Sequential([
        LSTM(50, activation='relu', input_shape=(time_steps, features)),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=1)
    return model

def predict_future_speed(model, data, scaler, time_steps):
    last_X = scaler.transform(data[-time_steps:])
    last_X = last_X.reshape(1, time_steps, 1)
    predicted_speed_scaled = model.predict(last_X)
    predicted_speed = scaler.inverse_transform(predicted_speed_scaled)[0][0]
    return predicted_speed

# Load environment variables
load_dotenv()
uri = os.getenv("MONGODB_URL")
client = MongoClient(uri)
db = client['myDatabase']
user_collection = db['users']
username = "mmills6060"
user = user_collection.find_one({'username': username})
devices = user.get('devices', [])

# Future datetime for prediction
future_datetime = datetime.strptime('2024-04-30 12:00:00', '%Y-%m-%d %H:%M:%S')

for device in devices:
    device_name = device.get('device_name', 'Unknown Device')
    speeds = [float(speed) for speed in device.get('upload_network_speed', []) if isinstance(speed, (int, str, float)) and speed != '']
    timestamps = [datetime.strptime(ts, "%Y-%m-%d %H:%M:%S.%f") for ts in device.get('date_added', []) if ts]
    df = pd.DataFrame({'timestamp': timestamps, 'upload_speed': speeds})
    df.sort_values('timestamp', inplace=True)

    # Scale the features
    scaler = MinMaxScaler(feature_range=(0, 1))
    df['scaled_speed'] = scaler.fit_transform(df[['upload_speed']])

    # Prepare data for LSTM
    time_steps = 5
    X, y = create_dataset(df[['scaled_speed']], df['scaled_speed'], time_steps)
    
    try:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        # Build and train the model
        model = build_and_train_model(X_train, y_train, time_steps, 1)

        # Prediction
        last_points = df['upload_speed'].tail(time_steps).values.reshape(-1, 1)
        predicted_speed = predict_future_speed(model, last_points, scaler, time_steps)
    except ValueError as e:
        print(f"Skipping {device_name}: {e}")
        continue  # Skip to the next device

    # Plotting
    plt.figure(figsize=(10, 5))
    plt.plot(df['timestamp'], df['upload_speed'], label='Historical Upload Speeds', marker='o')
    plt.axvline(x=future_datetime, color='r', linestyle='--', label='Prediction Point')
    plt.plot(future_datetime, predicted_speed, 'ro', label=f'Predicted Upload Speed: {predicted_speed:.2f} Mbps')
    plt.title(f"Upload Speeds Prediction for {device_name}")
    plt.xlabel('Timestamp')
    plt.ylabel('Upload Speed (Mbps)')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

