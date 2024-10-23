from detector_utils.detect_humans import detect_humans
from PIL import Image
import streamlit as st
import tempfile

def upload_own_image():
    uploaded_image_path = st.file_uploader("Upload an image of your choice...", type=["jpg", "png", "jpeg"])

    if uploaded_image_path is not None:     
        img = Image.open(uploaded_image_path)

        # Convert the image to RGB mode if it's in RGBA mode
        if img.mode == 'RGBA':
            img = img.convert('RGB')

        # Save the uploaded image temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_file_name = temp_file.name
            img.save(temp_file_name)  # Save the image in the temp file

        # Detect the humans in the image and display the final image
        result_img_rgb, _ = detect_humans(temp_file_name)
        st.image(result_img_rgb, caption="Human Detection Results", use_column_width=True)