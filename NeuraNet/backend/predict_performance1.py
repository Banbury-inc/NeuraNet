
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




username = "mmills6060"


load_dotenv()
uri = os.getenv("MONGODB_URL")

client = MongoClient(uri)
db = client['myDatabase']
user_collection = db['users']
user = user_collection.find_one({'username': username})

devices = user.get('devices', [])
 

total_upload_speed = 0
total_download_speed = 0
total_gpu_usage = 0
total_cpu_usage = 0
total_ram_usage = 0
upload_speed_count = 0
download_speed_count = 0
gpu_usage_count = 0
cpu_usage_count = 0
ram_usage_count = 0



for index, device in enumerate(devices):
    upload_speeds = [float(speed) for speed in device.get('upload_network_speed', []) if isinstance(speed, (int, str, float)) and speed != '']
    download_speeds = [float(speed) for speed in device.get('download_network_speed', []) if isinstance(speed, (int, str, float)) and speed != '']
    gpu_usages = [float(usage) for usage in device.get('gpu_usage', []) if isinstance(usage, (int, str, float)) and usage != '']
    cpu_usages = [float(usage) for usage in device.get('cpu_usage', []) if isinstance(usage, (int, str, float)) and usage != '']
    ram_usages = [float(usage) for usage in device.get('ram_usage', []) if isinstance(usage, (int, str, float)) and usage != '']
    date_added = [datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S.%f").timestamp() for date_string in device.get('date_added', []) if isinstance(date_string, str) and date_string != '']
    readable_dates = [datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S') for ts in date_added]
    upload_speed_count = len(upload_speeds) + 1
    download_speed_count = len(download_speeds) + 1
    gpu_usage_count = len(gpu_usages) + 1
    cpu_usage_count = len(cpu_usages) + 1
    ram_usage_count = len(ram_usages) + 1
    average_upload_speed = total_upload_speed / upload_speed_count if upload_speed_count else 0
    average_download_speed = total_download_speed / download_speed_count if download_speed_count else 0
    average_gpu_usage = total_gpu_usage / gpu_usage_count if gpu_usage_count else 0
    average_cpu_usage = total_cpu_usage / cpu_usage_count if cpu_usage_count else 0
    average_ram_usage = total_ram_usage / ram_usage_count if ram_usage_count else 0
    try:
        online = device.get('online')
    except Exception as e:
        print("online attribute doesn't exist, skipping")

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


data = {
    'timestamp': pd.date_range(start='2022-01-01', periods=100, freq='D'),
    'upload_speed': np.random.rand(100) * 100  # Random upload speeds
}

df = pd.DataFrame(data)
df['timestamp'] = pd.to_datetime(df['timestamp'])

scaler = MinMaxScaler(feature_range=(0, 1))
df['upload_speed_scaled'] = scaler.fit_transform(df[['upload_speed']])

def create_dataset(X, y, time_steps=1):
    Xs, ys = [], []
    for i in range(len(X) - time_steps):
        v = X.iloc[i:(i + time_steps)].values
        Xs.append(v)
        ys.append(y.iloc[i + time_steps])
    return np.array(Xs), np.array(ys)

time_steps = 10
X, y = create_dataset(df[['upload_speed_scaled']], df['upload_speed_scaled'], time_steps)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)




model = Sequential([
    LSTM(50, activation='relu', input_shape=(X_train.shape[1], X_train.shape[2])),
    Dense(1)
])
model.compile(optimizer='adam', loss='mean_squared_error')

model.summary()


history = model.fit(X_train, y_train, epochs=20, batch_size=32, validation_split=0.1, verbose=1)


loss = model.evaluate(X_test, y_test, verbose=2)


predictions = model.predict(X_test)

predictions_inverse = scaler.inverse_transform(predictions)
y_test_inverse = scaler.inverse_transform(y_test.reshape(-1, 1))

print("Predicted vs Actual Upload Speeds:")
for i in range(5):
    print(f"Predicted: {predictions_inverse[i][0]}, Actual: {y_test_inverse[i][0]}")

plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(loc='upper right')
plt.show()



