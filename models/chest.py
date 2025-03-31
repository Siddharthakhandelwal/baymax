import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img
import pandas as pd
import numpy as np
from tensorflow.keras import layers, models
from PIL import Image, ImageFile
import requests
import os
import subprocess
from fastapi import FastAPI, HTTPException

# Allow truncated images
ImageFile.LOAD_TRUNCATED_IMAGES = True

# Define the image preprocessing function
def load_preprocessed_image(image_path, img_height=180, img_width=180):
    img = Image.open(image_path).convert('RGB')
    img = img.resize((img_height, img_width))
    img_array = np.array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

app = FastAPI()

@app.post("/mri")
def mri():
    # Define image dimensions here
    img_height = 180
    img_width = 180
    
    # Download the image
    subprocess.run(["curl", "-o", "image.jpg", "https://bay-max-alpha.vercel.app/api/latest-pdf"])
    
    # Use the correct variable name img_path instead of image_path
    img_path = "image.jpg"
    
    # Load and preprocess the image
    preprocessed_img = load_preprocessed_image(img_path, img_height, img_width)
    
    # Load the model
    model = models.load_model("bone.h5")
    
    # Make predictions
    predictions = model.predict(preprocessed_img)
    
    # Process predictions
    predicted_class = (predictions > 0.5).astype("int32")
    class_names = ['fractured', 'not fractured']
    result = class_names[predicted_class[0][0]]
    
    print(f"Predicted class: {result}")
    
    # Send result to UI
    url = "https://baymax-ui.vercel.app/api/data"
    data = {
        "text": result,
    }
    response = requests.post(url, json=data)
    print(response.text)
    
    # Return the result as part of the API response
    return {"prediction": result, "confidence": float(predictions[0][0])}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)