import os
import json
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator

train_dir = '/Users/apple/Downloads/VS-code/PlantHealthAINew/Dataset/train'
val_dir = '/Users/apple/Downloads/VS-code/PlantHealthAINew/Dataset/validation'
model_path = 'models/plant_health_model.h5'  

if os.path.exists(model_path):
    print("Model exists skip training")
    exit()  
else:
    print("Train new model")
# just augmentation
# ImageDataGenerator class ensures that the model receives new variations of the images at each epoch. 
datagen = ImageDataGenerator(
    rescale=1./255,         
    rotation_range=20,      
    shear_range=0.2,        
    zoom_range=0.2,         
    horizontal_flip=True    
)
# labels subfolder in dataset
# both loading & augmentation here (loads images in 32 img batch)
# basically creates batches of aug images
train_data = datagen.flow_from_directory(
    train_dir,
    target_size=(128, 128),
    batch_size=32, 
    class_mode='categorical'
)
# saves labels to a JSON file 
labels_out = os.path.join("Python", "models", "class_indices.json")
os.makedirs(os.path.dirname(labels_out), exist_ok=True)  
with open(labels_out, "w") as f:
    json.dump(train_data.class_indices, f, indent=2)
print("Labels saved:", labels_out)

val_data = datagen.flow_from_directory(
    val_dir,
    target_size=(128, 128),
    batch_size=32,
    class_mode='categorical'
)
num_classes = train_data.num_classes
# actual model (MobileNetV2) here
# I removed top classification layers of it so that I can add mine
base_model = tf.keras.applications.MobileNetV2(
    input_shape=(128, 128, 3),
    include_top=False, 
    weights='imagenet' 
)
base_model.trainable = False # telling it not to train it's base layers
# adding my Layers
model = tf.keras.models.Sequential([
    base_model,
    tf.keras.layers.GlobalAveragePooling2D(),    
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.4),                 
    tf.keras.layers.Dense(num_classes, activation='softmax')  
])
# compiling the model
# adam learns things quickly like which weight to change
# Adaptive Moment estimation
model.compile(optimizer='adam', 
              loss='categorical_crossentropy',
              metrics=['accuracy'])

history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=10
)
# running trained model on validation data 
val_loss, val_accuracy = model.evaluate(val_data)
print(f"Validation loss: {val_loss}")
print(f"Validation accuracy: {val_accuracy}")

# accuracy graph
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()
# loss graph
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

model.save('models/plant_health_model.h5')