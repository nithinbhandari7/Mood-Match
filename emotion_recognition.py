import sys
import io
import base64
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.backend import clear_session

# Load the model
model = load_model('emotion_model.keras')

# Label mapping
label_dict = {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'sad', 5: 'surprise', 6: 'neutral'}

def preprocess_image(image_data):
    # Convert base64 to PIL Image
    image_data = image_data.split(',')[1]  # Remove the 'data:image/jpeg;base64,' part
    image = Image.open(io.BytesIO(base64.b64decode(image_data)))
    
    # Convert to grayscale and resize
    image = image.convert('L')  # Convert to grayscale
    image = image.resize((48, 48))  # Resize to match model input size
    
    # Convert to numpy array and preprocess
    image_array = np.array(image)
    image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension
    image_array = np.expand_dims(image_array, axis=-1)  # Add channel dimension
    image_array = image_array / 255.0  # Normalize pixel values
    
    return image_array

def predict_emotion(image_array):
    predictions = model.predict(image_array)
    emotion_index = np.argmax(predictions)  # Get the index of the highest probability
    return emotion_index

def get_emotion_label(emotion_index):
    return label_dict.get(emotion_index, 'unknown')

if __name__ == "__main__":
    image_data = sys.argv[1]  # Get the base64 image data from command-line argument
    image_array = preprocess_image(image_data)
    emotion_index = predict_emotion(image_array)
    emotion_label = get_emotion_label(emotion_index)
    print(emotion_label)  # Print the emotion label, which Node.js will capture
    clear_session()