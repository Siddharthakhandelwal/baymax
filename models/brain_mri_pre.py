import tensorflow as tf
from tensorflow.keras import datasets, layers, models # type: ignore
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.models import load_model #type:ignore
import matplotlib.pyplot as plt
import os
import subprocess
from fastapi import FastAPI, HTTPException

# app = FastAPI()
# @app.post("/mri")

def mri():
    #model to classify the image 
    # subprocess.run(["curl", "-o", "newfilename.jpg", "https://bay-max-alpha.vercel.app/api/latest-pdf"])
    img_path = "newfilename.jpg"
    class_labels = ['Glioma', 'Meningioma', 'Notumar', 'Piuitary']  # Replace with actual class names
    model = load_model('Brain.h5')
    def preprocess_image(img_path, target_size=(224, 224)):
        img = tf.keras.utils.load_img(img_path, target_size=(224, 224))
        img_array = tf.keras.utils.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0  # Rescaling the image
        return img_array

    def predict_mri(img_path):
        img_array = preprocess_image(img_path)
        prediction = model.predict(img_array)
        predicted_class = np.argmax(prediction, axis=1)
        return predicted_class

    def display_prediction(img_path, class_labels):
        img = tf.keras.utils.load_img(img_path, target_size=(224, 224))
        predicted_class = predict_mri(img_path)
        return f"Predicted class: {class_labels[predicted_class[0]]}"
    
    result=display_prediction(img_path,class_labels)
   
    subprocess.run(["curl", "-X", "POST", "https://baymax-ui.vercel.app/api/data", "-H", "Content-Type: application/json", "-d", f'{{"text": "{result}"}}'])

    print(result)

# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=5000)
mri()