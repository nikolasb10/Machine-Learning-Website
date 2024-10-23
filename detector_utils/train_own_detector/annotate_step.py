import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import pandas as pd
from general_utils.custom_write import custom_write
import shutil
import os
from detector_utils.train_own_detector.create_dataset_step import create_train_and_test_sets

### Helper Functions
def next_button_clicked():
    if st.session_state.image_index < len(st.session_state.uploaded_files) - 1:
        st.session_state.image_index += 1

def previous_button_clicked():
    if st.session_state.image_index > 0:
        st.session_state.image_index -= 1

def convert_to_yolo_format(bounding_box, img_width, img_height, class_label=0):
    # Get the coordinates of the bounding box
    left   = bounding_box["left"]
    top    = bounding_box["top"]
    width  = bounding_box["width"]
    height = bounding_box["height"]

    # Calculate the center coordinates (x_center, y_center)
    x_center = left + width / 2
    y_center = top + height / 2

    # Normalize the coordinates (between 0 and 1)
    x_center_norm = x_center / img_width
    y_center_norm = y_center / img_height
    width_norm    = width / img_width
    height_norm   = height / img_height

    # Return in YOLO format (class, x_center, y_center, width, height)
    return [class_label, x_center_norm, y_center_norm, width_norm, height_norm]

def load_existing_annotations():
    st.session_state.current_step = 4
    source_folder      = "./detector_utils/train_own_detector/own_detector_dataset/labels_wheelchair"
    destination_folder = "./detector_utils/train_own_detector/own_detector_dataset/labels"

    # Loop through all files in the source folder
    for filename in os.listdir(source_folder):
        source_file = os.path.join(source_folder, filename)
        destination_file = os.path.join(destination_folder, filename)
        
        # Only copy files (not subdirectories)
        if os.path.isfile(source_file):
            # Copy the file to the destination folder, replacing if it already exists
            shutil.copy2(source_file, destination_file)

    create_train_and_test_sets(base_dir="./detector_utils/train_own_detector/own_detector_dataset")

### 

def annotate_step():
    custom_write("Step 2: Annotate images with bounding boxes",20)
    uploaded_files = st.session_state.uploaded_files

    if st.session_state.demo_dataset_loaded:
        custom_write("With the wheelchair dataset you can load the existing annotations if you like!")

        st.button("Load existing annotations", on_click=load_existing_annotations)

    # Check if there are any uploaded files
    if uploaded_files:
        # Get the current image index
        current_image_index = st.session_state.image_index
        total_images        = len(uploaded_files)

        # Display the current image and let the user draw on it
        current_image = uploaded_files[current_image_index]
        img           = Image.open(current_image)
        img_width, img_height = img.size

        # Create layout with two columns: left for image, right for buttons
        img_col, btn_col = st.columns([5, 2])  # Adjust proportions as needed

        with img_col:
            # Set up canvas for drawing the bounding boxes on the image
            canvas_result = st_canvas(
                fill_color="rgba(255, 165, 0, 0.3)",  # Transparent fill
                stroke_width=3,
                stroke_color="#FF0000",
                background_image=img,  # Set the current image as background
                update_streamlit=True,
                height=img.height,
                width=img.width,
                drawing_mode="rect",  # Let the user draw bounding boxes
                key=f"canvas_{current_image_index}",  # Unique key for each canvas
            )

        with btn_col:
            # Display the buttons vertically
            st.button("Previous Image", disabled=current_image_index == 0, on_click=previous_button_clicked)
            st.button("Next Image", disabled=current_image_index == total_images - 1, on_click=next_button_clicked) 
                
        # Save bounding box coordinates if drawn
        if canvas_result.json_data is not None:
            objects = canvas_result.json_data["objects"]

            with btn_col:
                st.write("Bounding boxes for this image:")
                new_bounding_boxes      = []
                new_bounding_boxes_yolo = []
                
                for obj in objects:
                    bounding_box = {
                        "left": obj["left"],
                        "top": obj["top"],
                        "width": obj["width"],
                        "height": obj["height"]
                    }
                    new_bounding_boxes.append(bounding_box)
                    new_bounding_boxes_yolo.append(convert_to_yolo_format(bounding_box, img_width, img_height, class_label=0))

                # Save the bounding boxes for the current image
                if current_image_index >= len(st.session_state.bounding_boxes):
                    st.session_state.bounding_boxes.append(new_bounding_boxes)
                    st.session_state.yolo_bounding_boxes.append(new_bounding_boxes_yolo)
                elif len(new_bounding_boxes) != 0:
                    st.session_state.bounding_boxes[current_image_index]      = new_bounding_boxes
                    st.session_state.yolo_bounding_boxes[current_image_index] = new_bounding_boxes_yolo

                df_current_bboxes = pd.DataFrame(st.session_state.bounding_boxes[current_image_index])
                st.dataframe(df_current_bboxes)  

        # Display progress at the bottom of the page
        st.write(f"Progress: Image {current_image_index + 1} of {total_images}")
             
    else:
        st.write("Please provide images to annotate or select the wheelchair dataset!")


