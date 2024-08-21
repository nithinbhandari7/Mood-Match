import os
import numpy as np
from PIL import Image

def load_images_from_folder(folder):
    images = []
    labels = []
    
    # Iterate through each emotion folder in the main folder
    for emotion in os.listdir(folder):
        emotion_folder = os.path.join(folder, emotion)
        
        if os.path.isdir(emotion_folder):
            # Iterate through each image in the emotion folder
            for filename in os.listdir(emotion_folder):
                img_path = os.path.join(emotion_folder, filename)
                img = Image.open(img_path).convert('L')  # Convert image to grayscale
                img = img.resize((48, 48))  # Resize to 48x48
                img_array = np.array(img)
                images.append(img_array)
                labels.append(emotion)  # Label is the name of the emotion folder

    return np.array(images), np.array(labels)

# Load training and testing data
train_folder = 'archive/train'
test_folder = 'archive/test'
train_images, train_labels = load_images_from_folder(train_folder)
test_images, test_labels = load_images_from_folder(test_folder)

# Save the data as numpy arrays
np.save('train_images.npy', train_images)
np.save('train_labels.npy', train_labels)
np.save('test_images.npy', test_images)
np.save('test_labels.npy', test_labels)
