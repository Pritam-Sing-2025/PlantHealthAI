import os
import json
import argparse
import numpy as np
import tensorflow as tf
import cv2
from tensorflow.keras.preprocessing import image

projectRoot = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
modelPath = os.path.join(projectRoot, "models", "plant_health_model.h5")
trainDirectory = os.path.join(projectRoot, "Dataset", "train")
labelsPath = os.path.join(projectRoot, "models", "class_indices.json")

def loadClassLabels():    
    if os.path.exists(labelsPath):
        with open(labelsPath, "r") as f:
            idx_map = json.load(f) 
        inv = [None] * len(idx_map)
        for cls, idx in idx_map.items():
            inv[idx] = cls
        if all(c is not None for c in inv):
            return inv
        
    if not os.path.isdir(trainDirectory):
        raise FileNotFoundError(f"Train directory not found to infer classes: {trainDirectory}")
    classes = [d for d in os.listdir(trainDirectory)
               if os.path.isdir(os.path.join(trainDirectory, d))]
    if not classes:
        raise RuntimeError(f"No class subfolders found in {trainDirectory}")
    classes.sort()
    return classes

def loadAndPreprocess(img_path, target_size=(128, 128)):
    img = image.load_img(img_path, target_size=target_size)
    x = image.img_to_array(img)
    x = x / 255.0
    x = np.expand_dims(x, axis=0)
    return x

def calculateDamageAndSeriousness(img_path):
    img = cv2.imread(img_path) # to BGR (default of OpenCV lib)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # to RGB
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV) # to HSV
    # HSV color range for brown/yellow diseased areas
    lower = np.array([10, 40, 20])
    upper = np.array([35, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    diseased_pixels = np.sum(mask > 0)
    total_pixels = img.shape[0] * img.shape[1]
    damage_percent = (diseased_pixels / total_pixels) * 100
    # seriousness
    if damage_percent < 20:
        seriousness = "Mild"
        seriousness_value = 0.5
    elif damage_percent < 50:
        seriousness = "Moderate"
        seriousness_value = 1.0
    else:
        seriousness = "High"
        seriousness_value = 1.5
    return damage_percent, seriousness, seriousness_value

def topNPreds(preds, labels, n=3):
    probs = preds[0]
    idxs = np.argsort(probs)[::-1][:min(n, len(labels))]
    return [(labels[i], float(probs[i])) for i in idxs]

def parse_args():
    parser = argparse.ArgumentParser(description="Predict plant health/disease from a leaf image.")
    parser.add_argument(
        "image",
        nargs="?",
        default=os.path.join(projectRoot, "TestImg", "tomato_diseased(septoriaLeafSpot).jpeg"),
        help="Path to the image file."
    )
    parser.add_argument(
        "--topNPreds", type=int, default=3,
        help="Show top-n predictions (default: 3)."
    )
    return parser.parse_args()

def main():
    args = parse_args()
    if not os.path.exists(modelPath):
        raise FileNotFoundError(f"Model not found: {modelPath}")
    if not os.path.exists(args.image):
        raise FileNotFoundError(f"Image not found: {args.image}")
    model = tf.keras.models.load_model(modelPath)
    class_labels = loadClassLabels()
    num_classes = model.output_shape[-1]
    if num_classes != len(class_labels):
        raise RuntimeError(
            f"Model outputs {num_classes} classes, but {len(class_labels)} labels were found."
        )
    x = loadAndPreprocess(args.image)
    preds = model.predict(x)
    results = topNPreds(preds, class_labels, n=args.topNPreds) # sorts topN results
    bestName, bestProb = results[0] 
    # only if result is diseased then go for seriousness
    # if healthy word not in bestName (i.e. label)
    if "healthy" in bestName.lower():
        health_status = "Healthy"
        damage_percent = 0
        seriousness = "None"
        seriousness_value = 0.0
    else:
        health_status = "Diseased"
        damage_percent, seriousness, seriousness_value = calculateDamageAndSeriousness(args.image)

    print(f"\nFinal Prediction: {health_status} by {bestProb:.2%} surety and it is {bestName} ")
    print(f"Damage Percentage: {damage_percent:.2f}%")
    print(f"Seriousness: {seriousness}")
    print(f"Seriousness Value: {seriousness_value}")

if __name__ == "__main__":
    main()