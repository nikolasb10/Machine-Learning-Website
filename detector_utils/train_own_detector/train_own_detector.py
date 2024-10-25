import streamlit as st
from general_utils.custom_write import custom_write
import streamlit as st
from detector_utils.train_own_detector.annotate_step import annotate_step
from detector_utils.train_own_detector.create_dataset_step import create_dataset_step
from detector_utils.train_own_detector.load_images_step import load_images_step
from detector_utils.train_own_detector.train_step import train_step

# Define the total number of steps
total_steps = 4

# Function to go to the next step
def next_step():
    # If it's in the first page save dataset
    if st.session_state.current_step == 1 and len(st.session_state.uploaded_files) > 0:
        st.session_state.dataset_saved = True
    if st.session_state.current_step < total_steps:
        st.session_state.current_step += 1
    
# Function to go to the previous step
def prev_step():
    if st.session_state.current_step > 1:
        st.session_state.current_step -= 1

# Function to display step content
def show_step(step):
    if step == 1:
        load_images_step()
    elif step == 2:
        annotate_step()
    elif step == 3:
        create_dataset_step()
    elif step == 4:
        train_step()

def train_own_detector():
    
    # Initialize session states
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 1  # Start at step 1
    if 'image_index' not in st.session_state:
        st.session_state.image_index = 0
    if 'bounding_boxes' not in st.session_state:
        st.session_state.bounding_boxes = []
    if 'yolo_bounding_boxes' not in st.session_state:
        st.session_state.yolo_bounding_boxes = []
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []
    if 'dataset_saved' not in st.session_state:
        st.session_state.dataset_saved  = False
    if 'demo_dataset_loaded' not in st.session_state:
        st.session_state.demo_dataset_loaded = False
    if 'own_detector_trained' not in st.session_state:
        st.session_state.own_detector_trained = False

    custom_write("In this page you can train your own object detection model!",25)
    custom_write("Follow the steps below to achieve this!",20)

    # Display a progress bar at the top
    progress = st.session_state.current_step / total_steps
    st.progress(progress)

    # Display the current step content
    show_step(st.session_state.current_step)

    # Create navigation buttons
    st.write("---")  # Horizontal line divider
    col1, col2, col3 = st.columns([1, 3, 1])

    with col1:
        if st.session_state.current_step > 1:
            st.button("Previous Step", on_click=prev_step, use_container_width=True)

    with col3:
        # Align the button to the right within the column
        st.markdown("<div style='text-align: right;'>", unsafe_allow_html=True)
        if st.session_state.current_step < total_steps:
            st.button("Next Step", on_click=next_step, use_container_width=True, disabled=(st.session_state.current_step==4))
        # elif st.session_state.current_step == total_steps:
        #     st.button("Train", on_click=train_step, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    