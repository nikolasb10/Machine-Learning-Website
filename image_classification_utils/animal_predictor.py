import streamlit as st
import torch
import torchvision.transforms as transforms
from PIL import Image
import requests

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

        # Perform inference with the pre-trained model
        with torch.no_grad():
            # Preprocess the image and convert it to a list
            image_tensor = transform(image).unsqueeze(0)  # Shape: [1, C, H, W]
            output       = model(image_tensor)
            # Get the predicted class
            predicted_class = torch.argmax(output, dim=1).item()

            # image_list = image_tensor.squeeze(0).tolist()  # Remove batch dimension and convert to list

            # # Define the FastAPI endpoint
            # url = "http://127.0.0.1:8000/search"

            # # Send the tensor as JSON data using a POST request
            # response = requests.post(url, json={"query": image_list})

            # # Check for errors in the response
            # if response.status_code != 200:
            #     print("Error:", response.status_code, response.text[:200])
            # else:
            #     output = response.json()
            #     predicted_class = torch.argmax(torch.tensor(output["output"]), dim=1).item()

        st.write(f"Predicted Class: {label_to_name[str(predicted_class)]}")