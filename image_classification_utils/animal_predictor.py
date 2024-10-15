import streamlit as st
import torch
import torchvision.transforms as transforms
from PIL import Image

def animal_predictor(model, selected_image_path):
    # Define a transform to preprocess the input image
    transform = transforms.Compose([
        transforms.Resize((227, 227)),  # Resize image to the required input size
        transforms.ToTensor(),  # Convert to tensor
    ])

    predict = st.button("Make prediction")

    if predict:
        label_to_name = {"0": "Elefante",
                         "1": "Farfalla",
                         "2": "Mucca"   ,
                         "3": "Pecora"  ,
                         "4": "Scoiattolo"}
        # Open the image
        image = Image.open(selected_image_path)

        # Preprocess the image
        image = transform(image).unsqueeze(0)  # Add batch dimension

        # Perform inference with the pre-trained model
        with torch.no_grad():
            output = model(image)

        # Get the predicted class
        predicted_class = torch.argmax(output, dim=1).item()

        st.write(f"Predicted Class: {label_to_name[str(predicted_class)]}")