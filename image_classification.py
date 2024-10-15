import streamlit as st
from PIL import Image
from image_classification_utils.animal_predictor import animal_predictor
from image_classification_utils.ROC_curves import ROC_curves
from image_classification_utils.PCA_reduction import PCA_reduction
from image_classification_utils.initialize_animal_predictor_model import initialize_animal_predictor_model
from image_classification_utils.show_confusion_matrix import show_confusion_matrix

def app():
    st.title("📷 Image Classification")
    # st.write("Find objects in images!")

    # Create tabs
    tabs = st.tabs(["🦋 Animal Classification", "🧠 Brain Tumor Classification"])

    # Human Detector Tab
    with tabs[0]:
        st.write("In this section the results of the training on an animal dataset are presented. The code used to produce them can be found on: https://www.kaggle.com/code/nikolasbenetos/animal-classification")
        
        st.write("The animal dataset is consisted of 5 different kind of animals shown below")

        # List of image paths or URLs
        image_paths = [
            "./image_classification_utils/sample_images/category_Elefante_3.jpg"  ,
            "./image_classification_utils/sample_images/category_Farfalla_8.jpg"  ,
            "./image_classification_utils/sample_images/category_Mucca_11.jpg"    ,
            "./image_classification_utils/sample_images/category_Pecora_2.jpg"    ,
            "./image_classification_utils/sample_images/category_Scoiattolo_4.jpg",
        ]     

        image_names = [f"{x.split('/')[-1]}" for x in image_paths]

        # Display the images in a grid format with selectable options
        cols = st.columns(len(image_paths))

        # Loop through images and display each one in its column
        for idx, path in enumerate(image_paths):
            with cols[idx]:
                category = image_names[idx].split("_")[1]
                st.write(f"Class: {category}")
                st.image(path, use_column_width=True)  # Display the image


        with st.expander("📈 Training Time Visualizations"):
            true_labels, predicted_labels, class_names = show_confusion_matrix()
            st.write("Below is shown the One-vs-all Area Under the Receiver Operating Characteristic Curve, for the 5 different classes.")
            ROC_curves(true_labels, predicted_labels, class_names)
            st.markdown("""
                The Receiver Operating Characteristic (ROC) Curve, as we can see plots the true positive rate (recall) on the y – axis and the false positive rate (probability of false alarm – FP / (TN +FP) on the x-axis.
                The Area Under the Curve (AUC) is a way to quantify a model’s ROC curve, by calculating the total area under it, 
                a metric that falls between zero and one, with a higher number meaning better classification performance. As we can see above, 
                the AUC metric for the Farfalla class curve is greater, meaning that it can achieve a better blend of precision and recall, 
                as we saw in the confusion matrix too. Generally, all the classes have a similar (low) false positive rate, but they differ on their true positive rate.

            """)
            PCA_reduction()
            st.markdown("""
                        In the graph above, we can see that the Farfalla class has been separated better,
                        hence the higher accuracy that the model has on the specific class. In addition, 
                        we can see separation between the other classes too, but not at such a high level.
                        """)

        with st.expander("🎯 Test the predictor"):
            image_options = ["Select an image..."] + image_names
            selected_image = st.selectbox("Select an image by name:", image_options)

            # Show the selected image to the user
            if selected_image != "Select an image...":
                st.write(f"Selected Image: {selected_image}")
                selected_image_path = f"./image_classification_utils/sample_images/{selected_image}"
                st.image(selected_image_path)
                model = initialize_animal_predictor_model()    

                if model:
                    animal_predictor(model, selected_image_path)
                else:
                    st.write("Wait till the predictor is loaded... (It might take a few minutes)")

        model = initialize_animal_predictor_model()

    # Upload Image tab content
    with tabs[1]:
        st.header("Upload Image")
        st.write("Upload an image to detect objects.")
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
        if uploaded_file is not None:
            st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)
            st.write("Detecting objects...")
