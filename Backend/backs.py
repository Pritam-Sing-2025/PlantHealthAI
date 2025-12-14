from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import os
import tensorflow as tf
import numpy as np
import json
import cv2
from tensorflow.keras.preprocessing import image

app = FastAPI()

projectRoot = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
modelPath = os.path.join(projectRoot, "models", "plant_health_model.h5")
trainDirectory = os.path.join(projectRoot, "Dataset", "train")
labelsPath = os.path.join(projectRoot, "models", "class_indices.json")

# Load model once
model = tf.keras.models.load_model(modelPath)

def loadClassLabels():
    if os.path.exists(labelsPath):
        with open(labelsPath, "r") as f:
            idx_map = json.load(f)
        inv = [None] * len(idx_map)
        for cls, idx in idx_map.items():
            inv[idx] = cls
        return inv
    return []

class_labels = loadClassLabels()


def loadAndPreprocess(img_path, target_size=(128, 128)):
    img = image.load_img(img_path, target_size=target_size)
    x = image.img_to_array(img) / 255.0
    return np.expand_dims(x, axis=0)


def calculateDamageAndSeriousness(img_path):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    lower = np.array([10, 40, 20])
    upper = np.array([35, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)

    diseased_pixels = np.sum(mask > 0)
    total_pixels = img.size // 3
    damage_percent = (diseased_pixels / total_pixels) * 100

    if damage_percent < 20:
        return damage_percent, "Mild", 0.5
    elif damage_percent < 50:
        return damage_percent, "Moderate", 1.0
    else:
        return damage_percent, "High", 1.5


@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    img_path = "temp.jpg"
    with open(img_path, "wb") as f:
        f.write(await file.read())

    x = loadAndPreprocess(img_path)
    preds = model.predict(x)[0]

    best_idx = np.argmax(preds)
    bestName = class_labels[best_idx]
    bestProb = float(preds[best_idx])

    if "healthy" in bestName.lower():
        damage_percent = 0
        seriousness = "None"
        seriousness_value = 0.0
        health_status = "Healthy"
    else:
        health_status = "Diseased"
        damage_percent, seriousness, seriousness_value = calculateDamageAndSeriousness(img_path)

    os.remove(img_path)

    return JSONResponse({
        "status": health_status,
        "prediction": bestName,
        "confidence": bestProb,
        "damage_percent": damage_percent,
        "seriousness": seriousness,
        "seriousness_value": seriousness_value
    })

@app.get("/")
def home():
    return {"message": "API is running!"}



#  uvicorn main:app --reload



















# from flask import Flask, request, jsonify
# import os
# import tensorflow as tf
# import numpy as np
# import json
# import cv2
# from tensorflow.keras.preprocessing import image

# app = Flask(__name__)

# projectRoot = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# modelPath = os.path.join(projectRoot, "models", "plant_health_model.h5")
# trainDirectory = os.path.join(projectRoot, "Dataset", "train")
# labelsPath = os.path.join(projectRoot, "models", "class_indices.json")

# model = tf.keras.models.load_model(modelPath)

# def loadClassLabels():
#     if os.path.exists(labelsPath):
#         with open(labelsPath, "r") as f:
#             idx_map = json.load(f)
#         inv = [None] * len(idx_map)
#         for cls, idx in idx_map.items():
#             inv[idx] = cls
#         return inv
#     return []

# class_labels = loadClassLabels()

# def loadAndPreprocess(img_path, target_size=(128, 128)):
#     img = image.load_img(img_path, target_size=target_size)
#     x = image.img_to_array(img) / 255.0
#     return np.expand_dims(x, axis=0)

# def calculateDamageAndSeriousness(img_path):
#     img = cv2.imread(img_path)
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

#     lower = np.array([10, 40, 20])
#     upper = np.array([35, 255, 255])
#     mask = cv2.inRange(hsv, lower, upper)

#     diseased_pixels = np.sum(mask > 0)
#     total_pixels = img.size // 3
#     damage_percent = (diseased_pixels / total_pixels) * 100

#     if damage_percent < 20:
#         return damage_percent, "Mild", 0.5
#     elif damage_percent < 50:
#         return damage_percent, "Moderate", 1.0
#     else:
#         return damage_percent, "High", 1.5

# @app.post("/predict")
# def predict():
#     if "file" not in request.files:
#         return jsonify({"error": "No file provided"}), 400

#     file = request.files["file"]
#     img_path = "temp.jpg"
#     file.save(img_path)

#     x = loadAndPreprocess(img_path)
#     preds = model.predict(x)[0]
#     best_idx = np.argmax(preds)
#     bestName = class_labels[best_idx]
#     bestProb = float(preds[best_idx])

#     if "healthy" in bestName.lower():
#         damage_percent = 0
#         seriousness = "None"
#         seriousness_value = 0.0
#         health_status = "Healthy"
#     else:
#         health_status = "Diseased"
#         damage_percent, seriousness, seriousness_value = calculateDamageAndSeriousness(img_path)

#     os.remove(img_path)

#     return jsonify({
#         "status": health_status,
#         "prediction": bestName,
#         "confidence": bestProb,
#         "damage_percent": damage_percent,
#         "seriousness": seriousness,
#         "seriousness_value": seriousness_value
#     })

# if __name__ == "__main__":
#     app.run(debug=True)
