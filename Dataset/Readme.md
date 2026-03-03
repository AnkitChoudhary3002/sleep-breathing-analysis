## Dataset drive link

https://drive.google.com/drive/folders/1GR8_TI8vAaFfVWgvTrYecMiBVj-ZUJsj?usp=drive_link

## Generated Dataset

After running the pipeline, the following files are generated in `Dataset/`:

```
Dataset/
├── breathing_dataset_AP01.csv    # Windowed airflow data with labels
├── breathing_dataset_AP02.csv
├── breathing_dataset_AP03.csv
├── breathing_dataset_AP04.csv
├── breathing_dataset_AP05.csv
└── sleep_stage_dataset.csv       # Sleep stage labels for all participants
```

### Breathing Dataset Columns

| Column        | Description                              |
|---------------|------------------------------------------|
| `start_time`  | Window start timestamp                   |
| `end_time`    | Window end timestamp                     |
| `participant` | Participant ID (AP01–AP05)               |
| `label`       | Event label (Normal, Hypopnea, Apnea)    |
| `data`        | 960 samples (30s × 32Hz) as list         |
