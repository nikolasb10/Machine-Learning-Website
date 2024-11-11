import os
import pickle
import mediapipe as mp
import cv2
import streamlit as st
from general_utils.custom_write import custom_write
import os

def check_folder_structure(base_path, num_folders, num_images_per_folder):
    """
    Checks if a directory contains a specific number of folders, each named with increasing integers,
    and if each folder contains a specific number of .jpg files, also named with increasing integers.
    
    Args:
        base_path (str): Path to the main directory where folders should be located.
        num_folders (int): The number of expected folders, named as "0", "1", ..., up to num_folders - 1.
        num_images_per_folder (int): The expected number of .jpg files in each folder, named as "0.jpg", ..., up to num_images_per_folder - 1.

    Returns:
        bool: True if the structure is correct, False otherwise.
    """
    for folder_num in range(num_folders):
        # Construct the folder path for each numbered folder
        folder_path = f"{base_path}/{str(folder_num)}"
        print(folder_path)
        # Check if the folder exists
        if not os.path.isdir(folder_path):
            print(f"{folder_path} doesn't exist")
            return False
        
        # Check for the presence of each required image in the folder
        for image_num in range(num_images_per_folder):
            image_path = f"{folder_path}/{image_num}.jpg"
            
            if not os.path.isfile(image_path):
                print(f"{image_path} doesn't exist")
                return False
    return True

def create_dataset_proc(hands):
    DATA_DIR = st.session_state.data_dir

    data = []
    labels = []
    for dir_ in os.listdir(DATA_DIR):
        dir_path = f"{DATA_DIR}/{dir_}"
        # Check if the path is a directory (folder)
        if os.path.isdir(dir_path):
            for img_path in os.listdir(dir_path):
                data_aux = []

                x_ = []
                y_ = []

                img = cv2.imread(os.path.join(DATA_DIR, dir_, img_path))
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                results = hands.process(img_rgb)
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        for i in range(len(hand_landmarks.landmark)):
                            x = hand_landmarks.landmark[i].x
                            y = hand_landmarks.landmark[i].y

                            x_.append(x)
                            y_.append(y)

                        for i in range(len(hand_landmarks.landmark)):
                            x = hand_landmarks.landmark[i].x
                            y = hand_landmarks.landmark[i].y
                            data_aux.append(x - min(x_))
                            data_aux.append(y - min(y_))

                    data.append(data_aux)
                    labels.append(dir_)

    if len(data) > 0:
        f = open(f'{st.session_state.data_dir}/data.pickle', 'wb')
        pickle.dump({'data': data, 'labels': labels}, f)
        f.close()

def create_dataset():
    custom_write("Step 2: Create the dataset from the collected images.", 20)
    st.markdown("""
                    In this project instead of training a model with the collected images (image classification) we choose to work in the following way:
                
                    - We collect the hand landmarks of the gesture from each image using the MediaPipe architecture.
                    - We train a predictor of our choice (Random Forests, Logistic Regression, Decision Tree) on the created dataset of the hand features.
                """)
    
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

    isDataCollected = check_folder_structure(st.session_state.data_dir, st.session_state.number_of_classes, st.session_state.dataset_size)

    # If the demo dataset is loaded or the gesture frames haven't been collected then disable the create dataset button
    disableCreateDatasetButton = st.session_state.demo_dataset_loaded or (not isDataCollected) 
    st.button("Create dataset", on_click=create_dataset_proc, args=(hands,), disabled=disableCreateDatasetButton)

    if st.session_state.demo_dataset_loaded:
        st.write("(Dataset already created for demo dataset)")
    elif not isDataCollected:
        st.write("(Collect the images for your dataset creation or choose the demo dataset)")


    