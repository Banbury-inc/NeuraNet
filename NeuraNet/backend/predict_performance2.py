
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def create_dataset(X, y, time_steps=1):
    Xs, ys = [], []
    for i in range(len(X) - time_steps):
        v = X.iloc[i:(i + time_steps)].values
        Xs.append(v)
        ys.append(y.iloc[i + time_steps])
    return np.array(Xs), np.array(ys)


def predict_future_speed(df, model, scaler, future_datetime, time_steps=10):
    # Filter data up to a point before the prediction date
    filtered_df = df[df['timestamp'] < future_datetime]

    if len(filtered_df) < time_steps:
        print("Not enough data points available for prediction.")
        return None

    # Create scaled dataset for prediction
    filtered_df['upload_speed_scaled'] = scaler.fit_transform(filtered_df[['upload_speed']])

    # Extract last time_steps data points
    last_X = filtered_df['upload_speed_scaled'][-time_steps:].values
    last_X = last_X.reshape(1, time_steps, 1)

    # Predict upload speed for the future date
    predicted_speed_scaled = model.predict(last_X)
    predicted_speed = scaler.inverse_transform(predicted_speed_scaled)[0][0]

    return predicted_speed


# Load environment variables (assuming you have them set up for MongoDB access)
load_dotenv()
uri = os.getenv("MONGODB_URL")

# Connect to MongoDB
client = MongoClient(uri)
db = client['myDatabase']
user_collection = db['users']

# Get user data (assuming 'username' is defined elsewhere)
username = "mmills6060"  # Replace with your username
user = user_collection.find_one({'username': username})

devices = user.get('devices', [])

# Initialize variables to store resource usage
total_upload_speed = 0
total_download_speed = 0
total_gpu_usage = 0
total_cpu_usage = 0
total_ram_usage = 0

# Counters for resource usage data
upload_speed_count = 0
download_speed_count = 0
gpu_usage_count = 0
cpu_usage_count = 0
ram_usage_count = 0

# Process device data
for index, device in enumerate(devices):
    upload_speeds = [float(speed) for speed in device.get('upload_network_speed', []) if
                     isinstance(speed, (int, str, float)) and speed != '']
    download_speeds = [float(speed) for speed in device.get('download_network_speed', []) if
                       isinstance(speed, (int, str, float)) and speed != '']
    gpu_usages = [float(usage) for usage in device.get('gpu_usage', []) if
                  isinstance(usage, (int, str, float)) and usage != '']
    cpu_usages = [float(usage) for usage in device.get('cpu_usage', []) if
                  isinstance(usage, (int, str, float)) and usage != '']
    ram_usages = [float(usage) for usage in device.get('ram_usage', []) if
                  isinstance(usage, (int, str, float)) and usage != '']
    date_added = [datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S.%f").timestamp() for date_string in
                  device.get('date_added', []) if isinstance(date_string, str) and date_string != '']
    readable_dates = [datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S') for ts in date_added]

    # Update counters (assuming you want to use them elsewhere in your code)
    upload_speed_count += len(upload_speeds)
    download_speed_count += len(download_speeds)
    gpu_usage_count += len(gpu_usages)
    cpu_usage_count += len(cpu_usages)
    ram_usage_count += len(ram_usages)

    # Print data (optional, for debugging purposes)
    print("upload speeds")
    print(upload_speeds)
    print("download speeds")
    print(download_speeds)
    print("gpu_usages")
    print(gpu_usages)
    print("cpu_usages")
    print(cpu_usages)
    print("ram_usages")
    print(ram_usages)
    print("date_added")
    print(date_added)
    print("readable_dates")
    print(readable_dates)

# Create a dataframe with past upload speeds
data = {
    'timestamp': pd.date_range(start='2024-03-20', periods=100, freq='D'),
    'upload_speed': np.random.rand(100) * 100  # Random upload speeds
}

df = pd.DataFrame(data)

# Include time in the timestamp
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Create a scaler for normalizing data
scaler = MinMaxScaler(feature_range=(0, 1))

# Split data into features (X) and target (y)
X = df[['upload_speed']]
y = df['upload_speed']

# Scale the features
X_scaled = scaler.fit_transform(X)

# Convert the scaled features and target into a dataset suitable for LSTM
X_lstm, y_lstm = create_dataset(pd.DataFrame(X_scaled), pd.DataFrame(y))

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_lstm, y_lstm, test_size=0.2, random_state=42)

# Define the LSTM model
model = Sequential([
    LSTM(50, activation='relu', input_shape=(X_train.shape[1], X_train.shape[2])),
    Dense(1)
])

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
history = model.fit(X_train, y_train, epochs=20, batch_size=32, validation_split=0.1, verbose=1)

# Make predictions for the future
future_datetime = datetime.strptime('2024-07-25 12:00:00', '%Y-%m-%d %H:%M:%S')  # Specify future datetime
predicted_speed = predict_future_speed(df, model, scaler, future_datetime)

# Plot past upload speeds and predicted speed
plt.figure(figsize=(10, 6))
plt.plot(df['timestamp'], df['upload_speed'], label='Past Upload Speeds')
plt.axvline(x=future_datetime, color='r', linestyle='--', label='Future Timestamp')
plt.plot(future_datetime, predicted_speed, 'ro', label='Predicted Upload Speed')
plt.xlabel('Timestamp')
plt.ylabel('Upload Speed (Mbps)')
plt.title('Past Upload Speeds and Future Prediction')
plt.legend()
plt.grid(True)
plt.show()
