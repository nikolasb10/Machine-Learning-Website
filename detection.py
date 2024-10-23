import streamlit as st
from detector_utils.upload_own_image import upload_own_image
from detector_utils.choose_existing_image import choose_existing_image
from detector_utils.train_own_detector.train_own_detector import train_own_detector
from general_utils.custom_write import custom_write

def app():
    st.title("🕵️‍♂️ Object Detector")
    # st.write("Find objects in images!")

    # Create tabs
    tabs = st.tabs(["Human Detector", "Train your own detector"])

    # Human Detector Tab
    with tabs[0]:
        custom_write("Welcome to the Human Detector!",25)
        custom_write("Choose how you'd like to provide the image for detection.", 20)

        # Radio button for image source selection
        option = st.radio("Select Image Source:", ["Choose an existing image", "Upload your own image"])

        # If user selects to upload their own image
        if option == "Upload your own image":
            upload_own_image()

        # If user selects to choose from existing images
        elif option == "Choose an existing image":
            choose_existing_image()

    # Upload Image tab content
    with tabs[1]:
        train_own_detector()
