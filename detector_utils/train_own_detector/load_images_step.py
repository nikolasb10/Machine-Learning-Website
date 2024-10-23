import streamlit as st
from general_utils.custom_write import custom_write
import streamlit as st
import kagglehub
import os
import time
import random
from io import BytesIO

@st.cache_data
def load_kaggle_dataset():
    # Download the dataset from Kaggle
    dataset_path = kagglehub.dataset_download("yinchuangsum/person-wheel-chair-not-wheel-chair")

    # Define the folder where the images are stored after download
    images_folder = f"{dataset_path}\\valid\\images"

    return images_folder

def clear_dataset():
    st.session_state.dataset_saved        = False
    st.session_state.bounding_boxes       = []
    st.session_state.yolo_bounding_boxes  = []
    st.session_state.image_index          = 0
    st.session_state.own_detector_trained = False

def use_wheelchair_dataset(images_folder):
    # Load wheelchair dataset images into st.session_state.uploaded_files
    st.session_state.uploaded_files = []
    st.session_state.dataset_saved  = True
    st.session_state.demo_dataset_loaded = True
    image_names = []
    with open("./detector_utils/train_own_detector/wheel_chair_image_names.txt", "r") as file:
        for line in file:
            image_names.append(line.strip())

    for image_name in image_names:
        image_path = os.path.join(images_folder, image_name)
        # Open the image, convert to BytesIO and append to the session state
        with open(image_path, 'rb') as img_file:
            file_bytes = BytesIO(img_file.read())
            file_bytes.name = image_name  # Assign a name to mimic uploaded files
            st.session_state.uploaded_files.append(file_bytes)


def load_images_step():
    custom_write("Step 1: Provide images that will be used for training", 20)
    st.markdown("""
                    In order to train your model to detect a desired object you first have to provide the images that it will be trained on.\n
                    Ideally, they have to portrait your desired object in different angles and with different backgrounds to improve robustness.
                """)
    
    images_folder = load_kaggle_dataset()
    images_folder = "/home/appuser/.cache/kagglehub/datasets/yinchuangsum/person-wheel-chair-not-wheel-chair/versions/1/valid/images"
    # st.link_button("View annotated dataset")
    with st.expander("View example images for wheel chair dataset"):
        image_names = []
        with open("./detector_utils/train_own_detector/wheel_chair_image_names.txt", "r") as file:
            for i, line in enumerate(file):
                image_names.append(line.strip())
        random.shuffle(image_names)

        number_of_images = 5
        cols = st.columns(number_of_images)

        # Loop through images and display each one in its column
        for idx, image_name in enumerate(image_names[:number_of_images]):
            with cols[idx]:
                image_path = f"{images_folder}/{image_name}"
                st.image(image_path, use_column_width=True)  

    if st.session_state.dataset_saved:
        st.button("Clear images", on_click=clear_dataset)
    else:
        st.session_state.uploaded_files = st.file_uploader("Upload your images", accept_multiple_files=True, type=["jpg", "png", "jpeg"])
        # st.button("Save dataset", on_click=save_dataset)

        # Button to use the wheelchair dataset images
        st.button("Use wheel chair dataset", on_click=use_wheelchair_dataset, args=(images_folder,))
        st.write("or use the wheel chair dataset!")

