import streamlit as st
from detector_utils.detect_humans import detect_humans
from PIL import Image
import tempfile

def app():
    st.title("🕵️‍♂️ Object Detector")
    # st.write("Find objects in images!")

    # Create tabs
    tabs = st.tabs(["Human Detector", "Train your own detector"])

    # Human Detector Tab
    with tabs[0]:
        st.write("Welcome to the Human Detector!")
        
        st.write("Choose how you'd like to provide the image for detection.")

        # Radio button for image source selection
        option = st.radio("Select Image Source:", ["Choose an existing image", "Upload your own image"])

        # If user selects to upload their own image
        if option == "Upload your own image":
            uploaded_image_path = st.file_uploader("Upload an image of your choice...", type=["jpg", "png", "jpeg"])

            if uploaded_image_path is not None:     
                img = Image.open(uploaded_image_path)

                # Save the uploaded image temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                    temp_file_name = temp_file.name
                    img.save(temp_file_name)  # Save the image in the temp file

                # Detect the humans in the image and display the final image
                result_img_rgb, _ = detect_humans(temp_file_name)
                st.image(result_img_rgb, caption="Human Detection Results", use_column_width=True)

        # If user selects to choose from existing images
        elif option == "Choose an existing image":
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

    # Upload Image tab content
    with tabs[1]:
        st.header("Upload Image")
        st.write("Upload an image to detect objects.")
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
        if uploaded_file is not None:
            st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)
            st.write("Detecting objects...")
