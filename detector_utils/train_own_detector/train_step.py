import streamlit as st
from ultralytics import YOLO
from general_utils.custom_write import custom_write
import os
from PIL import Image

# Set custom mlflow directory
os.environ['MLFLOW_TRACKING_URI'] = './detector_utils/mlflow_logs'
    
def train_step():
    custom_write("Step 3: Train the model",20)

    if st.session_state.dataset_saved:
        # Let the user choose the number of epochs and batch size
        epochs = st.number_input("Select number of epochs", min_value=5, max_value=50, value=5, step=1)
        batch  = st.number_input("Select batch size", min_value=2, max_value=16, value=4, step=1)

        st.write("(About 1min per epoch for dataset with ~50 images and batch size of 4)")

        if st.session_state.demo_dataset_loaded:
            custom_write("With the wheelchair dataset you can test an already trained model (for 20 epochs) if you like!",20)
            model_path = './detector_utils/train_own_detector/own_detector_training_results/Custom_training/weights/best.pt'
            model      = YOLO(model_path)    
            test_model(model)
            custom_write("Else you can train it again!",20)

        if st.button("Train"):#, on_click=training_procedure, args=(epochs,batch))        
            model       = YOLO("./detector_utils/yolo11n.pt")

            config_path = "./detector_utils/train_own_detector/own_detector_dataset/config.yaml"
            # config_path = "../pink_toy_dataset/config.yaml"
            results_dir = "./detector_utils/train_own_detector/own_detector_training_results/"

            # Run the training process
            with st.spinner('Training the model...'):
                model.train(
                    data=config_path,
                    epochs=epochs,
                    batch=batch,
                    plots=True,  
                    project=results_dir,
                    name="Custom_training",
                    exist_ok=True,

                )
            
            # After training completes, display the plots
            st.success("Training complete! Showing training results:")
            st.session_state.own_detector_trained = True
            
            # Path to the plot that YOLO generates (usually called "results.png")
            results_plot_path = os.path.join(results_dir, "Custom_training/results.png")
            
            # Check if the results file exists and display it
            if os.path.exists(results_plot_path):
                image = Image.open(results_plot_path)
                st.image(image, caption="Training Results Plot", use_column_width=True)
            else:
                st.error("Results plot not found. Please check the training directory.")

            custom_write("### Test the model with a sample image",20)

        if st.session_state.own_detector_trained:
            test_model(model)
    else:
        st.write("Please provide images to annotate or select the wheelchair dataset!")

def test_model(model):
    # Let the user upload an image for testing
    with st.expander("Choose on of the test images"):
        images_folder = "./detector_utils/train_own_detector/own_detector_dataset/testing_model_images"
        images        = os.listdir(images_folder)
        
        image_options = ["Select an image..."] + images
        selected_image = st.selectbox("Select an image by name:", image_options)

        # Show the selected image to the user
        if selected_image != "Select an image...":
            st.write(f"Selected Image: {selected_image}")
            selected_image_path = f"{images_folder}/{selected_image}"
       
            # Load the image with PIL
            image = Image.open(selected_image_path)
            result_image_path = "./detector_utils/train_own_detector/own_detector_training_results/test_image.jpg"
            # Run inference using the trained model
            with st.spinner('Running inference on the uploaded image...'):
                results = model.predict(source=image)  # Predict using the model
                results[0].save(filename=result_image_path)  # save to disk

            # Display inference result (usually saved in `runs/detect/predict/`)
            st.success("Inference complete! Showing results:")
        
            # Show the predicted image with bounding boxes
            result_image = Image.open(result_image_path)
            left_co, cent_co,last_co = st.columns([1,2,1])
            with cent_co:
                st.image(result_image, caption="Prediction Results", use_column_width=True)

    
