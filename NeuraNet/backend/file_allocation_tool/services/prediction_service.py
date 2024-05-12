import os
import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
import matplotlib.pyplot as plt

class PredictionService:
    def __init__(self):
        pass
    
    def create_dataset(self, X, y, time_steps=1):
        Xs, ys = [], []
        for i in range(len(X) - time_steps):
            v = X.iloc[i:(i + time_steps)].values
            Xs.append(v)
            ys.append(y.iloc[i + time_steps])
        return np.array(Xs), np.array(ys)

    def build_and_train_model(self, X_train, y_train, time_steps, features):
        model = Sequential([
            LSTM(50, activation='relu', input_shape=(time_steps, features)),
            Dense(1)
        ])
        model.compile(optimizer='adam', loss='mean_squared_error')
        model.fit(X_train, y_train, epochs=20, batch_size=32, verbose=1)
        return model

    def predict_future_speed(self, model, df, scaler, time_steps, data_type):
        data = df[[data_type]].tail(time_steps).values
        last_X_scaled = scaler.transform(data)
        last_X = last_X_scaled.reshape(1, time_steps, 1)
        predicted_speed_scaled = model.predict(last_X)
        predicted_speed = scaler.inverse_transform(predicted_speed_scaled)[0][0]
        return predicted_speed

    def plot_data(self, df, predicted, future_datetime, label, ylabel):
        plt.figure(figsize=(10, 5))
        plt.plot(df['timestamp'], df[label], label=f'Historical {label}', marker='o')
        plt.axvline(x=future_datetime, color='r', linestyle='--', label='Prediction Point')
        plt.plot(future_datetime, predicted, 'ro', label=f'Predicted {label}: {predicted:.2f}')
        plt.title(f'{label} Prediction')
        plt.xlabel('Timestamp')
        plt.ylabel(ylabel)
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def performance_data(self, devices, date, show_graph):
        # Assuming datetime_string is provided or calculated somewhere within this scope.

        # datetime_string = '2024-05-04 19:25:50.473372'
        datetime_string = date 
        future_datetime = datetime.strptime(datetime_string.split('.')[0], '%Y-%m-%d %H:%M:%S')

        performance_data = []

        for device in devices:
            device_name = device.get('device_name', 'Unknown Device')
            print(device_name)
            metrics = ['upload_network_speed', 'download_network_speed', 'gpu_usage', 'cpu_usage', 'ram_usage']
            dfs = {}

            for metric in metrics:
                print(metric)
                speeds = [float(speed) for speed in device.get(metric, []) if isinstance(speed, (int, str, float)) and speed != '']
                timestamps = [datetime.strptime(ts.split('.')[0], "%Y-%m-%d %H:%M:%S") for ts in device.get('date_added', []) if ts]
                df = pd.DataFrame({'timestamp': timestamps, metric: speeds})
                df.sort_values('timestamp', inplace=True)

                scaler = MinMaxScaler(feature_range=(0, 1))
                df['scaled'] = scaler.fit_transform(df[[metric]])

                time_steps = 5 if metric in ['download_network_speed', 'gpu_usage', 'cpu_usage', 'ram_usage'] else 50
                X, y = self.create_dataset(df[['scaled']], df['scaled'], time_steps)

                if X.size == 0:
                    print(f"Skipping {device_name}: not enough data points for training.")
                    continue

                X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)
                model = self.build_and_train_model(X_train, y_train, time_steps, 1)
                predicted_metric = self.predict_future_speed(model, df, scaler, time_steps, metric)

                dfs[metric] = df
                performance_data.append({
                    'device_name': device_name,
                    f'predicted_{metric}': predicted_metric
                })

                if show_graph:
                    self.plot_data(df, predicted_metric, future_datetime, metric, 'Speed' if 'speed' in metric else 'Usage (%)')

        if not show_graph:
            print(performance_data)

        return performance_data


    def performance_data_multiple_dates(self, devices, show_graph):
        # Assuming datetime_string is provided or calculated somewhere within this scope.

        # datetime_string = '2024-05-04 19:25:50.473372'
        datetime_string ='2024-05-4 19:25:50.473372'
        future_datetime = datetime.strptime(datetime_string.split('.')[0], '%Y-%m-%d %H:%M:%S')

        performance_data = []

        for device in devices:
            device_name = device.get('device_name', 'Unknown Device')
            print(device_name)
            metrics = ['upload_network_speed', 'download_network_speed', 'gpu_usage', 'cpu_usage', 'ram_usage']
            dfs = {}

            for metric in metrics:
                print(metric)
                speeds = [float(speed) for speed in device.get(metric, []) if isinstance(speed, (int, str, float)) and speed != '']
                timestamps = [datetime.strptime(ts.split('.')[0], "%Y-%m-%d %H:%M:%S") for ts in device.get('date_added', []) if ts]
                df = pd.DataFrame({'timestamp': timestamps, metric: speeds})
                df.sort_values('timestamp', inplace=True)

                scaler = MinMaxScaler(feature_range=(0, 1))
                df['scaled'] = scaler.fit_transform(df[[metric]])

                time_steps = 5 if metric in ['download_network_speed', 'gpu_usage', 'cpu_usage', 'ram_usage'] else 50
                X, y = self.create_dataset(df[['scaled']], df['scaled'], time_steps)

                if X.size == 0:
                    print(f"Skipping {device_name}: not enough data points for training.")
                    continue

                X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)
                model = self.build_and_train_model(X_train, y_train, time_steps, 1)
                predicted_metric = self.predict_future_speed(model, df, scaler, time_steps, metric)

                dfs[metric] = df
                performance_data.append({
                    'device_name': device_name,
                    f'predicted_{metric}': predicted_metric
                })

                if show_graph:
                    self.plot_data(df, predicted_metric, future_datetime, metric, 'Speed' if 'speed' in metric else 'Usage (%)')

        if not show_graph:
            print(performance_data)

        return performance_data



