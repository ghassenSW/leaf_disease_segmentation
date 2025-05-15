import streamlit as st
import numpy as np
import tensorflow as tf
from PIL import Image

# Load the model
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("unet_model.h5")

model = load_model()


# Page title haha
st.title("Leaf Disease Segmentation with U-Net")

# Upload an image
uploaded_file = st.file_uploader("Upload a leaf image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Read and preprocess the image
    image = Image.open(uploaded_file).convert('RGB')
    image = image.resize((128, 128))  # Use your input size
    image_array = np.array(image) / 255.0
    image_input = np.expand_dims(image_array, axis=0)

    # Predict the mask
    pred_mask = model.predict(image_input)[0]

    # Convert mask to binary
    binary_mask = (pred_mask > 0.5).astype(np.uint8) * 255  

    # Display results  
    st.subheader("Original Image")
    st.image(image, use_column_width=True)

    st.subheader("Predicted Mask")
    st.image(binary_mask, clamp=True, use_column_width=True)
