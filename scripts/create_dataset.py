import os           # ✅ ADDED
import argparse     # ✅ ADDED
import pandas as pd
from scipy.signal import butter, filtfilt

# Usage: python create_dataset.py -in_dir "E:/sleepbreath/Data" -out_dir "E:/sleepbreath/Dataset"
parser = argparse.ArgumentParser()
parser.add_argument('-in_dir',  type=str, required=True, help='E:/sleepbreath/Data')
parser.add_argument('-out_dir', type=str, required=True, help='E:/sleepbreath/Dataset')
args = parser.parse_args()

in_dir  = args.in_dir
out_dir = args.out_dir  

os.makedirs(out_dir, exist_ok=True)

def bandpass_filter(signal, fs=32, low=0.17, high=0.4):
    b, a = butter(4, [low/(fs/2), high/(fs/2)], btype='band')
    y = filtfilt(b, a, signal)
    return y

def create_windows(signal, times, window_size_sec, step_sec, fs):
    N = len(signal)
    win_size = int(window_size_sec * fs)
    step = int(step_sec * fs)
    windows = []
    win_times = []
    for start in range(0, N - win_size + 1, step):
        window = signal[start:start+win_size]
        windows.append(window)
        win_times.append(times[start])
    return windows, win_times

def label_window(win_start, win_end, events):
    for i, row in events.iterrows():
        ev_start, ev_end, ev_type = row['ev_start'], row['ev_end'], row['type']
        overlap_start = max(win_start, ev_start)
        overlap_end = min(win_end, ev_end)
        delta = (overlap_end - overlap_start).total_seconds()
        if delta > 15:
            return ev_type
    return 'Normal'

def interval_to_tuple(s):
    start, end = s.split('-')
    start = pd.to_datetime(start.strip(), format='%d.%m.%Y %H:%M:%S,%f')
    d = start.strftime('%d.%m.%Y')
    if len(end.strip().split(':')) == 3:
        end = pd.to_datetime(f"{d} {end.strip()}", format='%d.%m.%Y %H:%M:%S,%f')
    else:
        end = pd.to_datetime(end.strip(), format='%d.%m.%Y %H:%M:%S,%f')
    return start, end

for i in range(1, 6):
    print(f"Processing AP0{i}...")

    airflow = pd.read_csv(
        os.path.join(in_dir, f'AP0{i}', 'Flow.txt'),
        header=None, names=['ts', 'val'], skiprows=7, sep=';'
    )
    airflow['ts'] = pd.to_datetime(airflow['ts'].str.strip(), format='%d.%m.%Y %H:%M:%S,%f')
    airflow['val'] = pd.to_numeric(airflow['val'], errors='coerce')
    airflow = airflow.dropna()

    filtered = bandpass_filter(airflow['val'].values, fs=32, low=0.17, high=0.4)

    windows, win_times = create_windows(
        filtered,
        airflow['ts'].values,
        window_size_sec=30,
        step_sec=15,
        fs=32
    )

    events = pd.read_csv(
        os.path.join(in_dir, f'AP0{i}', 'Flow Events.txt'),
        header=None, names=['interval', 'duration', 'type', 'stage'],
        skiprows=4, sep=';'
    )
    events[['ev_start', 'ev_end']] = events.apply(
        lambda row: pd.Series(interval_to_tuple(row['interval'])), axis=1
    )

    rows = []
    for j, (window, win_start_time) in enumerate(zip(windows, win_times)):
        win_start_time = pd.to_datetime(win_start_time)
        win_end_time = win_start_time + pd.Timedelta(seconds=30)
        label = label_window(win_start_time, win_end_time, events)
        rows.append({
            'start_time': win_start_time,
            'end_time': win_end_time,
            'participant': f'AP0{i}',
            'label': label,
            'data': window.tolist()
        })

    df = pd.DataFrame(rows)

    df.to_csv(os.path.join(out_dir, f'breathing_dataset_AP0{i}.csv'), index=False)
    print(f"Saved: breathing_dataset_AP0{i}.csv  ({len(df)} windows)")

print("All participants processed!")