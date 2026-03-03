import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt

# Usage: python vis.py -name "Data/AP01"
parser = argparse.ArgumentParser()
parser.add_argument('-name', type=str, required=True, help='E:\\sleepbreath\\Data\\AP01')
args = parser.parse_args()

participant_folder = args.name
participant_name   = os.path.basename(participant_folder)  
print(f'Processing {participant_folder}...')

airflow_file     = os.path.join(participant_folder, 'Flow.txt')
thorax_file      = os.path.join(participant_folder, 'Thorac.txt')
spo2_file        = os.path.join(participant_folder, 'SPO2.txt')
flow_events_file = os.path.join(participant_folder, 'Flow Events.txt')

    # Load signals, skipping header metadata
airflow = pd.read_csv(airflow_file, header=None, names=['ts', 'val'], skiprows=7, sep=';')
thorax  = pd.read_csv(thorax_file,  header=None, names=['ts', 'val'], skiprows=7, sep=';')
spo2    = pd.read_csv(spo2_file,    header=None, names=['ts', 'val'], skiprows=7, sep=';')

    # Convert timestamps
airflow['ts'] = pd.to_datetime(airflow['ts'].str.strip(), format='%d.%m.%Y %H:%M:%S,%f')
thorax['ts']  = pd.to_datetime(thorax['ts'].str.strip(),  format='%d.%m.%Y %H:%M:%S,%f')
spo2['ts']    = pd.to_datetime(spo2['ts'].str.strip(),    format='%d.%m.%Y %H:%M:%S,%f')

    # Convert values to numbers, handle non-numeric
airflow['val'] = pd.to_numeric(airflow['val'], errors='coerce')
thorax['val']  = pd.to_numeric(thorax['val'],  errors='coerce')
spo2['val']    = pd.to_numeric(spo2['val'],    errors='coerce')

    # Load breathing events
flow_event = pd.read_csv(
    flow_events_file, header=None,
    names=['interval', 'duration', 'type', 'stage'],
    skiprows=4, sep=';'
)

    # Robust parsing for interval time
def interval_to_tuple(s):
    try:
        start, end = s.split('-')
        start = pd.to_datetime(start.strip(), format='%d.%m.%Y %H:%M:%S,%f')
        if len(end.strip().split(':')) == 3:
            d = start.strftime('%d.%m.%Y')
            end = pd.to_datetime(f"{d} {end.strip()}", format='%d.%m.%Y %H:%M:%S,%f')
        else:
            end = pd.to_datetime(end.strip(), format='%d.%m.%Y %H:%M:%S,%f')
        return start, end
    except Exception as e:
        print(f"Failed to parse interval: {s} ({e})")
        return pd.NaT, pd.NaT

event_ranges = [interval_to_tuple(row['interval']) for _, row in flow_event.iterrows()]
event_types  = flow_event['type'].values

os.makedirs(r"E:\sleepbreath\Visualizations", exist_ok=True)
pdf_filename = os.path.join(f"E:\\sleepbreath\\Visualizations\\{participant_name}_visualization.pdf")
  
fig, axs = plt.subplots(3, 1, sharex=True, figsize=(20, 8))
axs[0].plot(airflow['ts'], airflow['val'], label='Nasal Airflow')
axs[1].plot(thorax['ts'],  thorax['val'],  label='Thoracic Movement')
axs[2].plot(spo2['ts'],    spo2['val'],    label='SpO₂')
for ax in axs:
    ax.legend()

    # Overlay events
for (start, end), typ in zip(event_ranges, event_types):
    if pd.isnull(start) or pd.isnull(end):
        continue
    color = 'red' if 'Apnea' in typ else 'orange' if 'Hypopnea' in typ else 'white'
    for ax in axs:
        ax.axvspan(start, end, color=color, alpha=0.3)
    
from matplotlib.patches import Patch

red_box = Patch(facecolor='red', alpha=0.4, label='Apnea')
orange_box = Patch(facecolor='orange', alpha=0.4, label='Hypopnea')
event_legend = [red_box, orange_box]
axs[0].legend(handles=event_legend, loc='upper right')

fig.suptitle(f"{participant_name} Sleep Signals and Breathing Events")
plt.xlabel("Time")
plt.tight_layout()
plt.savefig(pdf_filename)
print(f"PDF saved to: {pdf_filename}")
plt.close()

print("Visualization done!")