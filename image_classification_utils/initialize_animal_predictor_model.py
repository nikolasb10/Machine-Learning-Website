import gdown
from image_classification_utils.AlexNet import AlexNet
import torch
import os
import streamlit as st

@st.cache_resource
def initialize_animal_predictor_model():
    # Define the path where the model will be stored locally
    model_path = './image_classification_utils/model_weights/AlexNet_best_weights.pth'
    folder_path = './image_classification_utils/model_weights'

    # Google Drive URL of the model (replace 'YOUR_FILE_ID' with the actual file ID from Google Drive link)
    model_url = 'https://drive.google.com/uc?id=12e9z8EIC1RrOPdnwEoj8Sw3RDWPj9C1i'

    # Check if the folder contains any files or subdirectories
    folder_content = [f for f in os.listdir(folder_path) if f != '.gitkeep']
    if len(folder_content) == 0:
        # Folder is empty start downloading weights
        with st.spinner('Loading the predictor...'):
            gdown.download(model_url, model_path, quiet=False)
    else:
        # Folder not empty check if it has finished downloading (if path exists)
        if not os.path.exists(model_path):
            # it hasn't finished downloading
            return 0

    # Load the pre-trained model weights
    model = AlexNet()
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()

    return model