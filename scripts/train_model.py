import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense

#  usage: python train_model.py
all_dfs = []
for i in range(1, 6):
    path = f"E:/sleepbreath/Dataset/breathing_dataset_AP0{i}.csv"
    df_i = pd.read_csv(path)
    all_dfs.append(df_i)

df = pd.concat(all_dfs, ignore_index=True)
print(f"Total windows: {len(df)}")
print(f"Label counts:\n{df['label'].value_counts()}")

print("Unique participants:", df['participant'].unique())

X = np.stack(df['data'].apply(eval).values)
y = df['label'].values
participants = df['participant'].str.strip().values  

le = LabelEncoder()
le.fit(y)
y_encoded = le.transform(y)

all_participants = [f'AP0{i}' for i in range(1, 6)]

all_y_true = []
all_y_pred = []

for test_participant in all_participants:
    print(f"\n--- Fold: Test = {test_participant} ---")

    test_mask  = participants == test_participant  
    train_mask = participants != test_participant   

    X_train = X[train_mask]
    y_train = y_encoded[train_mask]
    X_test  = X[test_mask]
    y_test  = y_encoded[test_mask]

    print(f"Train windows: {len(X_train)}  |  Test windows: {len(X_test)}")

    model = Sequential([
        Conv1D(filters=16, kernel_size=5, activation='relu', input_shape=(X_train.shape[1], 1)),
        MaxPooling1D(pool_size=2),
        Flatten(),
        Dense(64, activation='relu'),
        Dense(len(le.classes_), activation='softmax')
    ])

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    model.fit(X_train[..., np.newaxis], y_train, epochs=10, batch_size=32, validation_split=0.2, verbose=0)

    y_pred = model.predict(X_test[..., np.newaxis])
    y_pred_classes = np.argmax(y_pred, axis=1)
    print(f"y_test length: {len(y_test)}")
    print(f"y_pred_classes length: {len(y_pred_classes)}")
    print(f"y_test unique values: {np.unique(y_test)}")

    
    present_labels = np.unique(np.concatenate([y_test, y_pred_classes]))
    print(f"Results for {test_participant}:")
    print(classification_report(
        y_test,
        y_pred_classes,
        target_names=le.classes_[present_labels],  
        labels=present_labels                    
    ))

    all_y_true.extend(y_test)
    all_y_pred.extend(y_pred_classes)
print("\n========== OVERALL RESULTS (All 5 Participants) ==========")
print(classification_report(all_y_true, all_y_pred, target_names=le.classes_))

cm = confusion_matrix(all_y_true, all_y_pred)
plt.figure(figsize=(5, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=le.classes_, yticklabels=le.classes_)
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix - Leave-One-Participant-Out')
plt.tight_layout()
plt.show()