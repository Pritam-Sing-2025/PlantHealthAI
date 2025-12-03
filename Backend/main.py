import io
import json
import numpy as np
import cv2
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import tensorflow as tf

app = FastAPI()

MODEL_PATH = "models/plant_health_model.h5"
LABELS_PATH = "models/class_indices.json"

model = tf.keras.models.load_model(MODEL_PATH)

# Load labels
with open(LABELS_PATH, "r") as f:
    class_indices = json.load(f)
index_to_label = {v: k for k, v in class_indices.items()}

def calculate_damage_and_seriousness(image: Image.Image):
    img = np.array(image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    lower = np.array([10, 40, 20])
    upper = np.array([35, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    diseased_pixels = np.sum(mask > 0)
    total_pixels = img.shape[0] * img.shape[1]
    damage_percent = (diseased_pixels / total_pixels) * 100
    if damage_percent < 20:
        seriousness = "Mild"
        seriousness_value = 0.5
    elif damage_percent < 50:
        seriousness = "Moderate"
        seriousness_value = 1.0
    else:
        seriousness = "High"
        seriousness_value = 1.5
    return round(damage_percent, 2), seriousness, seriousness_value

# approx cost cal
def estimate_cost(seriousness):
    if seriousness == "None":
        return "No cost. Plant is healthy."
    elif seriousness == "Mild":
        return "Estimated cost: ₹50 - ₹150"
    elif seriousness == "Moderate":
        return "Estimated cost: ₹150 - ₹350"
    elif seriousness == "High":
        return "Estimated cost: ₹350 - ₹700"
    else:
        return "Cost unavailable"

remedies = {
    "healthy": "Plant is healthy, just keepon pouring water.",
    "early_blight": "Leaves are diseased with early blight, do xyz thing.",
    "late_blight": "Leaves are diseased with late blight, do xyz thing.",
    "leaf_spot": "Leaf spot is found, do xyz thing.",
    "bacterial_spot": "Backtorial spot found, do xyz thing.",
    "leaf_mold": "Leaf mold found, do xyz thing."
} 

# prediction
def predict_image(image: Image.Image):
    img = image.resize((128, 128))
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    preds = model.predict(img)
    best_index = np.argmax(preds[0])
    confidence = float(preds[0][best_index]) * 100
    best_label = index_to_label[best_index]
    return best_label, confidence

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    best_label, confidence = predict_image(image)
    if "healthy" in best_label.lower():
        damage_percent = 0.0
        seriousness = "None"
        seriousness_value = 0.0
    else:
        damage_percent, seriousness, seriousness_value = calculate_damage_and_seriousness(image)
    cost = estimate_cost(seriousness)
    remedy_key = best_label.lower().replace("___", "_")
    remedy = remedies.get(remedy_key, "Do xyz things.")
    return {
        "prediction": best_label,
        "confidence": round(confidence, 2),
        "damage_percent": damage_percent,
        "seriousness": seriousness,
        "seriousness_value": seriousness_value,
        "approx_cost": cost,
        "remedies": remedy
    }

@app.get("/")
def home():
    return {"message": "Plant Health Detection API is running!"}

# swagger ui