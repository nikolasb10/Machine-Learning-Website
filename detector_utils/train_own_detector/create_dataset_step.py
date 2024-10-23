import streamlit as st
from general_utils.custom_write import custom_write
import pandas as pd
import os
import random
import shutil

### Helper Functions
# Flatten the bounding boxes for better table display
def get_bounding_boxes_dataframe(bounding_boxes_all_images):
    flattened_data = []
    for img_index, bounding_boxes in enumerate(bounding_boxes_all_images):
        for bbox in bounding_boxes:
            flattened_data.append({
                "Image Index": img_index + 1,  # Start from 1 instead of 0 for user-friendliness
                "Left": bbox['left'],
                "Top": bbox['top'],
                "Width": bbox['width'],
                "Height": bbox['height']
            })

    # Convert the flattened data into a DataFrame
    df = pd.DataFrame(flattened_data)
    return df

def create_labels_files(base_dir):
    # Ensure the output directory exists
    labels_dir = f"{base_dir}/labels"
    if not os.path.exists(labels_dir):
        os.makedirs(labels_dir)

    for index_image, image_bboxes in enumerate(st.session_state.yolo_bounding_boxes):
        output_filepath = f"{labels_dir}/{index_image}.txt"
        with open(output_filepath, "w") as file:
            for bbox in image_bboxes:
                file.write(f"{bbox[0]} {bbox[1]:.6f} {bbox[2]:.6f} {bbox[3]:.6f} {bbox[4]:.6f}\n")

def clear_folder(folder_path):
    """
    Deletes all files in the specified folder.
    """
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Remove the file
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Remove the directory
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

# Function to copy images and labels to train/test directories with index as the file name
def move_files(indices, images_dir, labels_dir, base_dir):
    for i in indices:
        image = st.session_state.uploaded_files[i]
        
        # New name based on the index of the image
        image_name = f"{i}.jpg"
        label_name = f"{i}.txt"
        
        # Save the image in the corresponding directory
        image_path = f"{images_dir}/{image_name}"
        with open(image_path, "wb") as f:
            f.write(image.getbuffer())

        # Move the corresponding label file if it exists
        label_src = f"{base_dir}/labels/{label_name}"
        if os.path.exists(label_src):
            label_dst = f"{labels_dir}/{label_name}"
            shutil.copy(label_src, label_dst)
        else:
            st.write(f"Label file for {image_name} not found")

def create_train_and_test_sets(train_split=0.8, base_dir="dataset"):
    # Create necessary directories for train and test sets
    train_images_dir, train_labels_dir = os.path.join(base_dir, "images/train"), os.path.join(base_dir, "labels/train")
    test_images_dir , test_labels_dir  = os.path.join(base_dir, "images/val"), os.path.join(base_dir, "labels/val")

    os.makedirs(train_images_dir, exist_ok=True)
    os.makedirs(train_labels_dir, exist_ok=True)
    os.makedirs(test_images_dir, exist_ok=True)
    os.makedirs(test_labels_dir, exist_ok=True)

    clear_folder(train_images_dir)
    clear_folder(test_images_dir)
    clear_folder(train_labels_dir)
    clear_folder(test_labels_dir)

    # Shuffle the images randomly and split into train/test sets
    total_images = len(st.session_state.uploaded_files)
    indices = list(range(total_images))
    random.shuffle(indices)
    
    train_size = int(train_split * total_images)
    train_indices = indices[:train_size]
    test_indices  = indices[train_size:]

    # Move files for train set
    move_files(train_indices, train_images_dir, train_labels_dir, base_dir)

    # Move files for test set
    move_files(test_indices, test_images_dir, test_labels_dir, base_dir)

    return len(train_indices), len(test_indices)

def create_dataset():
    create_labels_files(base_dir="./detector_utils/train_own_detector/own_detector_dataset")
    train_size, test_size = create_train_and_test_sets(base_dir="./detector_utils/train_own_detector/own_detector_dataset")

    st.write(f"Train set size: {train_size} images")
    st.write(f"Test set size: {test_size} images")
    st.button("Download dataset folder")

###
                
def create_dataset_step():
    custom_write("Step 3: Review and Convert Images to dataset (Not used if demo dataset annotations loaded)",20)

    if st.session_state.dataset_saved:
        st.write("Review your chosen bounding boxes and press the convert button to create the dataset folder.")
        st.write("Bounding boxes for all images:")

        bounding_boxes = get_bounding_boxes_dataframe(st.session_state.bounding_boxes)

        st.dataframe(bounding_boxes, hide_index=True)

        if not st.session_state.demo_dataset_loaded:
            st.button("Convert", on_click=create_dataset)
    else:
        st.write("Please provide images to annotate or select the wheelchair dataset!")

