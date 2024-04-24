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

show_graph = True

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
    model.fit(X_train, y_train, epochs=20, batch_size=32, verbose=1)
    return model

def predict_future_speed(model, df, scaler, time_steps, data_type):
    # Extract the last `time_steps` of scaled data as a NumPy array
    data = df[[data_type]].tail(time_steps).values
    last_X_scaled = scaler.transform(data)
    
    # Ensure last_X_scaled is correctly shaped for LSTM prediction
    # No need to use create_dataset function here since we only need the last sequence
    last_X = last_X_scaled.reshape(1, time_steps, 1)
    
    # Predict upload speed for the future date
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
    upload_speeds = [float(speed) for speed in device.get('upload_network_speed', []) if isinstance(speed, (int, str, float)) and speed != '']
    download_speeds = [float(speed) for speed in device.get('download_network_speed', []) if isinstance(speed, (int, str, float)) and speed != '']
    timestamps = [datetime.strptime(ts, "%Y-%m-%d %H:%M:%S.%f") for ts in device.get('date_added', []) if ts]
    df_upload_speed = pd.DataFrame({'timestamp': timestamps, 'upload_speed': upload_speeds})
    df_download_speed = pd.DataFrame({'timestamp': timestamps, 'download_speed': download_speeds})
    df_upload_speed.sort_values('timestamp', inplace=True)
    df_download_speed.sort_values('timestamp', inplace=True)

    # Scale the features
    scaler = MinMaxScaler(feature_range=(0, 1))
    df_upload_speed['scaled_speed'] = scaler.fit_transform(df_upload_speed[['upload_speed']])

    time_steps = 5  # Length of input sequences
    X, y = create_dataset(df_upload_speed[['scaled_speed']], df_upload_speed['scaled_speed'], time_steps)
    
    if X.size == 0:
        print(f"Skipping {device_name}: not enough data points for training.")
        continue
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = build_and_train_model(X_train, y_train, time_steps, 1)
    predicted_upload_speed = predict_future_speed(model, df_upload_speed, scaler, time_steps, data_type='upload_speed')

    df_download_speed['scaled_speed'] = scaler.fit_transform(df_download_speed[['download_speed']])

    time_steps = 5  # Length of input sequences
    X, y = create_dataset(df_download_speed[['scaled_speed']], df_download_speed['scaled_speed'], time_steps)
    
    if X.size == 0:
        print(f"Skipping {device_name}: not enough data points for training.")
        continue
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = build_and_train_model(X_train, y_train, time_steps, 1)
    predicted_download_speed = predict_future_speed(model, df_download_speed, scaler, time_steps, data_type='download_speed')


    # Plotting
    plt.figure(figsize=(10, 5))
    plt.plot(df_upload_speed['timestamp'], df_upload_speed['upload_speed'], label='Historical Upload Speeds', marker='o')
    plt.plot(df_download_speed['timestamp'], df_download_speed['download_speed'], label='Historical Download Speeds', marker='o')
    plt.axvline(x=future_datetime, color='r', linestyle='--', label='Prediction Point')
    plt.plot(future_datetime, predicted_upload_speed, 'ro', label=f'Predicted Upload Speed: {predicted_upload_speed:.2f} Mbps')
    plt.plot(future_datetime, predicted_download_speed, 'ro', label=f'Predicted Download Speed: {predicted_download_speed:.2f} Mbps')
    plt.title(f"Upload Speeds Prediction for {device_name}")
    plt.xlabel('Timestamp')
    plt.ylabel('Upload and Download Speed (Mbps)')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)

for device in devices:
    device_name = device.get('device_name', 'Unknown Device')
    gpu_usage = [float(speed) for speed in device.get('gpu_usage', []) if isinstance(speed, (int, str, float)) and speed != '']
    cpu_usage = [float(speed) for speed in device.get('cpu_usage', []) if isinstance(speed, (int, str, float)) and speed != '']
    ram_usage = [float(speed) for speed in device.get('ram_usage', []) if isinstance(speed, (int, str, float)) and speed != '']
    timestamps = [datetime.strptime(ts, "%Y-%m-%d %H:%M:%S.%f") for ts in device.get('date_added', []) if ts]
    df_gpu_usage = pd.DataFrame({'timestamp': timestamps, 'gpu_usage': gpu_usage})
    df_cpu_usage = pd.DataFrame({'timestamp': timestamps, 'cpu_usage': cpu_usage})
    df_ram_usage = pd.DataFrame({'timestamp': timestamps, 'ram_usage': ram_usage})
    df_gpu_usage.sort_values('timestamp', inplace=True)
    df_cpu_usage.sort_values('timestamp', inplace=True)
    df_ram_usage.sort_values('timestamp', inplace=True)

    time_steps = 5  # Length of input sequences
    # Scale the features
    scaler = MinMaxScaler(feature_range=(0, 1))
    df_gpu_usage['scaled_speed'] = scaler.fit_transform(df_gpu_usage[['gpu_usage']])
    df_cpu_usage['scaled_speed'] = scaler.fit_transform(df_cpu_usage[['cpu_usage']])
    df_ram_usage['scaled_speed'] = scaler.fit_transform(df_ram_usage[['ram_usage']])

    X, y = create_dataset(df_gpu_usage[['scaled_speed']], df_gpu_usage['scaled_speed'], time_steps)
    if X.size == 0:
        print(f"Skipping {device_name}: not enough data points for training.")
        continue
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = build_and_train_model(X_train, y_train, time_steps, 1)
    predicted_gpu_usage = predict_future_speed(model, df_gpu_usage, scaler, time_steps, data_type='gpu_usage')


    X, y = create_dataset(df_cpu_usage[['scaled_speed']], df_cpu_usage['scaled_speed'], time_steps)
    if X.size == 0:
        print(f"Skipping {device_name}: not enough data points for training.")
        continue
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = build_and_train_model(X_train, y_train, time_steps, 1)
    predicted_cpu_usage = predict_future_speed(model, df_cpu_usage, scaler, time_steps, data_type='cpu_usage')

    X, y = create_dataset(df_ram_usage[['scaled_speed']], df_ram_usage['scaled_speed'], time_steps)
    if X.size == 0:
        print(f"Skipping {device_name}: not enough data points for training.")
        continue
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = build_and_train_model(X_train, y_train, time_steps, 1)
    predicted_ram_usage = predict_future_speed(model, df_ram_usage, scaler, time_steps, data_type='ram_usage')



    # Plotting
    plt.figure(figsize=(10, 5))
    plt.plot(df_gpu_usage['timestamp'], df_gpu_usage['gpu_usage'], label='Historical GPU Usage %', marker='o')
    plt.plot(df_cpu_usage['timestamp'], df_cpu_usage['cpu_usage'], label='Historical CPU Usage %', marker='o')
    plt.plot(df_ram_usage['timestamp'], df_ram_usage['ram_usage'], label='Historical RAM Usage %', marker='o')
    plt.axvline(x=future_datetime, color='r', linestyle='--', label='Prediction Point')
    plt.plot(future_datetime, predicted_gpu_usage, 'ro', label=f'Predicted GPU Usage %: {predicted_gpu_usage:.2f} %')
    plt.plot(future_datetime, predicted_cpu_usage, 'ro', label=f'Predicted CPU Usage %: {predicted_cpu_usage:.2f} %')
    plt.plot(future_datetime, predicted_ram_usage, 'ro', label=f'Predicted RAM Usage %: {predicted_ram_usage:.2f} %')
    plt.title(f"Performance Prediction for {device_name}")
    plt.xlabel('Timestamp')
    plt.ylabel('GPU, CPU, and RAM Usage %')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)

if show_graph:
    plt.tight_layout()
    plt.show()

