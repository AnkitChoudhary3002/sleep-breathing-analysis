from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Conv1D, MaxPooling1D, Flatten, Dense

def build_cnn_model(input_length, num_classes):
    """
    Build a simple 1D CNN model for sleep breathing event classification.
    
    Args:
        input_length : number of samples in each window (e.g. 960 = 30sec * 32Hz)
        num_classes  : number of output classes (e.g. 5)
    
    Returns:
        Compiled Keras model
    """
    model = Sequential([
        Input(shape=(input_length, 1)),           # ✅ fixes the UserWarning
        Conv1D(filters=16, kernel_size=5, activation='relu'),
        MaxPooling1D(pool_size=2),
        Flatten(),
        Dense(64, activation='relu'),
        Dense(num_classes, activation='softmax')
    ])

    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    return model