import streamlit as st
from PIL import Image
from detector_utils.detect_humans import detect_humans

def choose_existing_image():
    # Expander for image selection
    with st.expander("Choose an existing Image"):
        image_files = {
            "Image 1": "./detector_utils/images/human_detection1.jpg",
            "Image 2": "./detector_utils/images/human_detection2.jpg",
            "Image 3": "./detector_utils/images/human_detection3.jpg"
        }

        image_options = ["Select an image..."] + list(image_files.keys())

        # Display all the images for preview
        cols = st.columns(len(image_files))
        for idx, (name, path) in enumerate(image_files.items()):
            with cols[idx]:
                image = Image.open(path)
                st.image(image, caption=name, use_column_width=True)

        # Selectbox to choose an image
        selected_image = st.selectbox("Select an image by name:", image_options)

        if selected_image != "Select an image...":
            image_path = image_files[selected_image]
            result_img_rgb, _ = detect_humans(image_path)
            # Display the image with human detections in RGB format
            st.image(result_img_rgb, caption="Human Detection Results", use_column_width=True)