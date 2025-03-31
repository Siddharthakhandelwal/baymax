import tensorflow as tf
from tensorflow.keras import datasets, layers, models # type: ignore
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.preprocessing import image # type: ignore
def predict_xray_image(model, img_path):
    img = image.load_img(img_path, target_size=(150, 150))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0
    prediction = model.predict(img_array)

    if prediction[0] > 0.5:
        result = 'Positive'
    else:
        result = 'Negative'



loaded_model = tf.keras.models.load_model('Chest-X_Ray_inc.h5')
# Example usage of the prediction functionperson1_virus_6.jpeg
img_path ='brain.jpg'
predict_xray_image(loaded_model, img_path)
