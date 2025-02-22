import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt
import os
model_path = "bone_xray.h5"  
model = tf.keras.models.load_model(model_path)

class_labels = ["No Fracture", "Fracture"]  

def preprocess_image(img_path, target_size=(224, 224)):
    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  
    return img_array

def predict_fracture(img_path):
    img_array = preprocess_image(img_path)
    prediction = model.predict(img_array)
    predicted_class = np.argmax(prediction, axis=1)[0]
    return class_labels[predicted_class]

# Example usage
image_path = "10-rotated1-rotated1-rotated2.jpg"  # Replace with your test image
predicted_label, confidence_score = predict_fracture(image_path)
print(f"Predicted: {predicted_label}")

from typing import Union
from fastapi import FastAPI
app = FastAPI()


@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Read the image bytes
        image_bytes = await file.read()
        
        # Convert to a numpy array
        image_array = np.asarray(bytearray(image_bytes), dtype=np.uint8)
        
        # Decode the image (assuming it's a bitmap or other valid image format)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        if image is None:
            return {"error": "Invalid image format"}