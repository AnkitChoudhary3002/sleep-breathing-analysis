# Sleep Breathing Analysis

A machine learning pipeline to detect and classify sleep breathing events (Apnea, Hypopnea) and sleep stages from polysomnography signals.

---

## Project Structure

```
sleepbreath/
├── Data/                        # Raw participant data (not included in repo)
│   ├── AP01/
│   │   ├── Flow.txt             # Nasal airflow signal (32 Hz)
│   │   ├── Thorac.txt           # Thoracic movement signal (32 Hz)
│   │   ├── SPO2.txt             # Blood oxygen signal (4 Hz)
│   │   ├── Flow Events.txt      # Annotated breathing events
│   │   └── Sleep profile.txt    # Sleep stage annotations (30s epochs)
│   ├── AP02/ ... AP05/
│
├── Dataset/                     # Generated CSV datasets
│   ├── breathing_dataset_AP01.csv
│   ├── breathing_dataset_AP02.csv
│   ├── breathing_dataset_AP03.csv
│   ├── breathing_dataset_AP04.csv
│   ├── breathing_dataset_AP05.csv
│   └── sleep_stage_dataset.csv
│
├── Visualizations/              # Generated PDF plots
│   ├── AP01_visualization.pdf
��   ├── AP02_visualization.pdf
│   ├── AP03_visualization.pdf
│   ├── AP04_visualization.pdf
│   └── AP05_visualization.pdf
│
├── models/
│   └── cnn_model.py             # 1D CNN model definition
│
├── scripts/
│   ├── vis.py                   # Visualize signals and events
│   ├── create_dataset.py        # Create breathing event dataset
│   ├── sleep_dataset.py         # Create sleep stage dataset
│   └── train_model.py           # Train CNN with Leave-One-Out CV
│
├── explore_data.py              # Data exploration script
├── data_analysis.md             # Data analysis findings
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

---

## Dataset

- **5 participants** (AP01–AP05)
- **Signals:** Nasal Airflow, Thoracic Movement, SpO₂
- **Breathing events:** Normal, Hypopnea, Obstructive Apnea, Mixed Apnea, Body event
- **Sleep stages:** Wake, N1, N2, N3, REM

---

## Pipeline

### Step 1 — Visualize Signals
Plot raw signals with breathing event overlays for one participant:
```bash
python scripts/vis.py -name "E:\sleepbreath\Data\AP01"
```

### Step 2 — Create Breathing Dataset
Segment airflow signal into 30-second windows with 15-second overlap and label each window:
```bash
python scripts/create_dataset.py -in_dir "E:\sleepbreath\Data" -out_dir "E:\sleepbreath\Dataset"
```

### Step 3 — Create Sleep Stage Dataset
Extract sleep stage labels from Sleep profile files:
```bash
python scripts/sleep_dataset.py -in_dir "E:\sleepbreath\Data" -out_dir "E:\sleepbreath\Dataset"
```

### Step 4 — Train Model
Train 1D CNN using Leave-One-Participant-Out Cross Validation:
```bash
python scripts/train_model.py
```

---

## Model

- **Architecture:** 1D Convolutional Neural Network (CNN)
- **Input:** 30-second airflow windows (960 samples at 32 Hz)
- **Layers:** Conv1D → MaxPooling1D → Flatten → Dense → Softmax
- **Evaluation:** Leave-One-Participant-Out Cross Validation (5 folds)

---

## Signal Preprocessing

- **Bandpass filter:** Butterworth 4th order, 0.17–0.4 Hz (breathing frequency range)
- **Window size:** 30 seconds
- **Window step:** 15 seconds (50% overlap)
- **Labelling:** Window is labelled with event type if overlap > 15 seconds, else Normal

---

## Requirements

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## Results

Model is evaluated per participant and overall using:
- Classification Report (Precision, Recall, F1-score)
- Confusion Matrix heatmap

---

## Authors
- Ankit Choudhary