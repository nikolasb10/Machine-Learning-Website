from gesture_recognition_utils.train_sign_detector.collect_images import collect_images
from gesture_recognition_utils.train_sign_detector.create_dataset import create_dataset
from gesture_recognition_utils.train_sign_detector.train_classifier import train_classifier
from gesture_recognition_utils.train_sign_detector.inference_detector import inference_detector
import streamlit as st
from general_utils.custom_write import custom_write

# Define the total number of steps
total_steps = 4

# Function to go to the next step
def next_step():
    if st.session_state.current_step_sign < total_steps:
        st.session_state.current_step_sign += 1
    
# Function to go to the previous step
def prev_step():
    if st.session_state.current_step_sign > 1:
        st.session_state.current_step_sign -= 1

# Function to display step content
def show_step(step):
    if step == 1:
        collect_images()
    elif step == 2:
        create_dataset()
    elif step == 3:
        train_classifier()
    elif step == 4:
        inference_detector() 
    
def train_sign_detector():
    # Initialize session states
    if 'current_step_sign' not in st.session_state:
        st.session_state.current_step_sign = 1  

    custom_write("Train your own gesture detector!",25)

    # Create navigation buttons
    st.write("---")  # Horizontal line divider

    # Display a progress bar at the top
    progress = st.session_state.current_step_sign / total_steps
    st.progress(progress, "Follow the steps below to achieve this!")

    # Display the current step content
    show_step(st.session_state.current_step_sign)
    
    col1, _ , col3 = st.columns([1, 3, 1])

    with col1:
        if st.session_state.current_step_sign > 1:
            st.button("Previous Step", on_click=prev_step, use_container_width=True)

    with col3:
        # Align the button to the right within the column
        st.markdown("<div style='text-align: right;'>", unsafe_allow_html=True)
        if st.session_state.current_step_sign < total_steps:
            st.button("Next Step", on_click=next_step, use_container_width=True, disabled=(st.session_state.current_step_sign==4))
        st.markdown("</div>", unsafe_allow_html=True)
    
    
    
