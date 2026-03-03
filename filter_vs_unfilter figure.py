import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import butter, filtfilt

def bandpass_filter(signal, fs=32, low=0.17, high=0.4):
    b, a = butter(4, [low/(fs/2), high/(fs/2)], btype='band')
    y = filtfilt(b, a, signal)
    return y

# Replace this with your actual file location and name
filepath = r"E:\sleepbreath\data\Ap01\Flow - 30-05-2024.txt"

# Load the CSV
airflow = pd.read_csv(
    filepath,
    header=None,
    names=['ts', 'val'],
    skiprows=7,
    sep=';'
)

# Convert values to numeric, drop rows with problems
airflow['val'] = pd.to_numeric(airflow['val'], errors='coerce')
airflow = airflow.dropna()

# Get first 3000 samples (optional, for plotting a short section)
signal = airflow['val'].values[:3000]

# Filter the signal
filtered = bandpass_filter(signal, fs=32, low=0.17, high=0.4)

# Plot
plt.figure(figsize=(12, 4))
plt.plot(signal, label='Original (Noisy)')
plt.plot(filtered, label='Filtered (Butterworth 0.17–0.4 Hz)')
plt.legend()
plt.xlabel('Sample number')
plt.ylabel('Airflow')
plt.title('Nasal Airflow: Filtered vs. Unfiltered')
plt.show()