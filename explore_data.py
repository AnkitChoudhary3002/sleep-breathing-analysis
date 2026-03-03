import os 
import pandas as pd

for i in range(1, 6):
    participant_folder = f'E:\\sleepbreath\\Data\\AP0{i}'

    files = os.listdir(participant_folder)
    print(files)
    print(f'============AP0{i}=============')
    print('nasal_flow')

    nasal_flow = pd.read_csv(os.path.join(participant_folder, 'Flow.txt'), sep=';', header=None, skiprows=7)
    print(nasal_flow.head())
    print(nasal_flow.shape)
    print(f"Non-null values per column:\n{nasal_flow.isnull().sum()}")
    print(f"\nData types:\n{nasal_flow.dtypes}")
    nasal_flow[1] = pd.to_numeric(nasal_flow[1], errors='coerce')
    print(nasal_flow[1].nunique())
    print('=========================')

    print('flow_events')

    flow_event = pd.read_csv(os.path.join(participant_folder, 'Flow Events.txt'), sep=';', header=None, skiprows=7)
    print(flow_event.head())
    print(flow_event.shape)
    print(f"\nData types:\n{flow_event.dtypes}")
    print(f"Non-null values per column:\n{flow_event.isnull().sum()}")
    flow_event[1] = pd.to_numeric(flow_event[1], errors='coerce')
    print(flow_event[1].value_counts())
    print(flow_event[2].value_counts())
    print(flow_event[3].value_counts())
    print('=========================')

    print('thoracic')
    thoracic = pd.read_csv(os.path.join(participant_folder, 'Thorac.txt'), sep=';', header=None, skiprows=7)
    print(thoracic.head())
    print(thoracic.shape)
    print(f"Non-null values per column:\n{thoracic.isnull().sum()}")
    print(f"\nData types:\n{thoracic.dtypes}")

    print('=========================')
    print('spO2')
    spO2 = pd.read_csv(os.path.join(participant_folder, 'SPO2.txt'), sep=';', header=None, skiprows=7)
    print(spO2.head())
    print(spO2.shape)
    print(f"Non-null values per column:\n{spO2.isnull().sum()}")
    print(f"\nData types:\n{spO2.dtypes}")

    print('=========================')
    print('sleep profile')
    sleep_profile = pd.read_csv(os.path.join(participant_folder, 'sleep profile.txt'), sep=';', header=None, skiprows=7)
    print(sleep_profile.head())
    print(sleep_profile.shape)
    print(f"Non-null values per column:\n{sleep_profile.isnull().sum()}")
    print(f"\nData types:\n{sleep_profile.dtypes}")
    print(sleep_profile[1].value_counts())

    print('=========================')