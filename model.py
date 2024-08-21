import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
from tensorflow.keras.layers import Dropout

# Load preprocessed data
X_train = np.load('train_images.npy')
y_train = np.load('train_labels.npy')
X_test = np.load('test_images.npy')
y_test = np.load('test_labels.npy')

# Preprocess labels (convert string labels to integer labels)
label_dict = {label: idx for idx, label in enumerate(sorted(set(y_train)))}
y_train = np.array([label_dict[label] for label in y_train])
y_test = np.array([label_dict[label] for label in y_test])

# Define the CNN model
def build_model():
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(48, 48, 1)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        Dropout(0.5),
        layers.Dense(len(label_dict), activation='softmax')  # Number of classes
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

# Build and train the model
model = build_model()
model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))
model.save('emotion_model.keras')