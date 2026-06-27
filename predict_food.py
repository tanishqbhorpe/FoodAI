import json
import numpy as np
import tensorflow as tf
from PIL import Image

from food_database import FOOD_DATABASE

# ============================================
# CONFIG
# ============================================

MODEL_PATH = "models/final/food_ai_model.keras"
CLASS_FILE = "models/final/class_names.json"
IMAGE_SIZE = (224, 224)

# ============================================
# LOAD CLASS NAMES
# ============================================

with open(CLASS_FILE, "r") as f:
    CLASS_NAMES = json.load(f)

# ============================================
# MODEL CACHE
# ============================================

_model = None


def load_model():
    """
    Loads the trained model only once.
    """

    global _model

    if _model is None:
        print("Loading AI Model...")
        _model = tf.keras.models.load_model(MODEL_PATH)
        print("Model Loaded Successfully.")

    return _model


# ============================================
# IMAGE PREPROCESSING
# ============================================

def preprocess_image(image_source):

    if isinstance(image_source, Image.Image):
        image = image_source.convert("RGB")

    else:
        image = Image.open(image_source).convert("RGB")

    image = image.resize(IMAGE_SIZE)

    image = np.array(image).astype("float32")

    image = tf.keras.applications.efficientnet.preprocess_input(image)

    image = np.expand_dims(image, axis=0)

    return image
# ============================================
# PREDICTION
# ============================================

def predict_food(image_source):

    model = load_model()

    image = preprocess_image(image_source)

    prediction = model.predict(image, verbose=0)[0]

    top3_indices = prediction.argsort()[-3:][::-1]

    confidence = float(prediction[top3_indices[0]]) * 100
    # Reject predictions with low confidence
    
    # ----------------------------------------

    if confidence >= 85:
        confidence_level = "High"

    elif confidence >= 70:
        confidence_level = "Medium"

    else:
        confidence_level = "Low"

    # ----------------------------------------

    top3 = []

    for idx in top3_indices:

        top3.append({

            "food": CLASS_NAMES[idx].replace("_", " ").title(),

            "confidence": round(float(prediction[idx]) * 100, 2)

        })

    # ----------------------------------------

    best_index = top3_indices[0]

# Unknown food detection
    best_index = top3_indices[0]

    food_key = CLASS_NAMES[best_index]

    info = FOOD_DATABASE.get(food_key, {})

    food_key = CLASS_NAMES[best_index]

    info = FOOD_DATABASE.get(food_key, {})

    # ----------------------------------------

    result = {

        "food": food_key.replace("_", " ").title(),

        "confidence": round(confidence, 2),

        "confidence_level": confidence_level,

        "serving": info.get("serving", "N/A"),

        "calories": info.get("calories", "N/A"),

        "description": info.get("description", "N/A"),

        "top3": top3

    }

    return result
# ============================================
# TEST
# ============================================

if __name__ == "__main__":

    image_path = input("Image Path : ").strip().strip('"')

    result = predict_food(image_path)

    print("\nPrediction\n")

    print(result)