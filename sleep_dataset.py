import os
import argparse
import pandas as pd

# Usage: python create_sleep_dataset.py -in_dir "E:\sleepbreath\Data" -out_dir "E:\sleepbreath\Dataset"
parser = argparse.ArgumentParser()
parser.add_argument('-in_dir',  type=str, required=True, help='Path to input data folder')
parser.add_argument('-out_dir', type=str, required=True, help='Path to output dataset folder')
args = parser.parse_args()

in_dir  = args.in_dir
out_dir = args.out_dir
os.makedirs(out_dir, exist_ok=True)

all_dfs = []

for i in range(1, 6):
    participant  = f'AP0{i}'
    sleep_file   = os.path.join(in_dir, participant, 'Sleep profile.txt')
    print(f"Processing {participant}...")

    df = pd.read_csv(
        sleep_file,
        header=None,
        names=['ts', 'stage'],
        skiprows=8,        
        sep=';'
    )

    df['ts'] = pd.to_datetime(df['ts'].str.strip(), format='%d.%m.%Y %H:%M:%S,%f')
    df['stage'] = df['stage'].str.strip()
    df['participant'] = participant

    print(f"  {len(df)} epochs found")
    print(f"  Stage counts:\n{df['stage'].value_counts()}\n")

    all_dfs.append(df)

combined = pd.concat(all_dfs, ignore_index=True)
print(f"Total epochs (all participants): {len(combined)}")
print(f"Overall stage counts:\n{combined['stage'].value_counts()}")

output_path = os.path.join(out_dir, 'sleep_stage_dataset.csv')
combined.to_csv(output_path, index=False)
print(f"\nSaved: {output_path}")