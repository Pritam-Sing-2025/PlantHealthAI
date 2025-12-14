import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os
import json

# BASE FOLDER = PlantHealthAINew/
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load labels from PlantHealthAINew/models/
LABELS_PATH = os.path.join(PROJECT_ROOT, "models", "class_indices.json")
with open(LABELS_PATH, "r") as f:
    class_labels = json.load(f)

# Load model from PlantHealthAINew/models/
MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "plant_health_model.h5")
model = tf.keras.models.load_model(MODEL_PATH)

# Correct model input size
IMG_SIZE = (128, 128)

def preprocess(img_bytes):
    image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    image = image.resize(IMG_SIZE)
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    return image

def predict_image(file_bytes):
    img = preprocess(file_bytes)
    preds = model.predict(img)[0]

    class_idx = int(np.argmax(preds))
    confidence = float(preds[class_idx])

    # ---------------------------
    # FIXED REVERSE MAPPING HERE
    # ---------------------------
    class_name = None
    for name, idx in class_labels.items():
        if int(idx) == class_idx:
            class_name = name
            break

    if class_name is None:
        raise ValueError(f"Class index {class_idx} not found in class_indices.json")

    # Healthy case
    if "healthy" in class_name.lower():
        return {
            "class": class_name,
            "confidence": confidence,
            "health_status": "Healthy",
            "damage_percent": 0,
            "seriousness": "None",
            "seriousness_value": 0
        }

    # Diseased case
    damage_percent = round((1 - confidence) * 100, 2)
    seriousness = "Severe" if confidence < 0.5 else "Moderate"
    seriousness_value = float(1 - confidence)

    return {
        "class": class_name,
        "confidence": confidence,
        "health_status": "Diseased",
        "damage_percent": damage_percent,
        "seriousness": seriousness,
        "seriousness_value": seriousness_value
    }
