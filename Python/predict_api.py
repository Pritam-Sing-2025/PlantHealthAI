import sys
import json
import os

# Disable ALL TensorFlow logging output
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
tf.get_logger().setLevel('ERROR')

import numpy as np
from prediction import (
    loadClassLabels,
    loadAndPreprocess,
    calculateDamageAndSeriousness
)

# Load model once
projectRoot = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
modelPath = os.path.join(projectRoot, "models", "plant_health_model.h5")

model = tf.keras.models.load_model(modelPath)
labels = loadClassLabels()

def predict_api(image_path):
    img = loadAndPreprocess(image_path)
    preds = model.predict(img, verbose=0)[0]     # <-- Stop TF printing

    best_idx = int(np.argmax(preds))
    best_label = labels[best_idx]
    best_prob = float(preds[best_idx])

    if "healthy" in best_label.lower() or best_prob < 0.50:
        status = "Healthy"
        damage = 0
        seriousness = "None"
    else:
        status = "Diseased"
        damage, seriousness, _ = calculateDamageAndSeriousness(image_path)

    return {
        "label": best_label,
        "probability": round(best_prob * 100, 2),
        "status": status,
        "damage": round(damage, 2),
        "seriousness": seriousness
    }

if __name__ == "__main__":
    image_path = sys.argv[1]
    result = predict_api(image_path)
    print(json.dumps(result))   # JSON ONLY (no extra prints)
