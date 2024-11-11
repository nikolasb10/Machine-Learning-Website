from gesture_recognition_utils.ImageCollectorProcessor import ImageCollectorProcessor
import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from general_utils.custom_write import custom_write
import os 

def start_class_capture(class_index):
    if st.session_state.processor:
        st.session_state.processor.start_capture(class_index, st.session_state.dataset_size)

def use_demo_dataset():
    st.session_state.demo_dataset_loaded = True
    st.session_state.dataset_created     = True

def clear_dataset():
    st.session_state.demo_dataset_loaded = False
    st.session_state.dataset_created     = True

def collect_images():
    if "data_dir" not in st.session_state:
        st.session_state.data_dir = './gesture_recognition_utils/train_sign_detector/data_directory'
    if "demo_dataset_loaded" not in st.session_state:
        st.session_state.demo_dataset_loaded = False
    if "dataset_size" not in st.session_state:
        st.session_state.dataset_size = 200
    if "number_of_classes" not in st.session_state:
        st.session_state.number_of_classes = 2
    if "processor" not in st.session_state:
        st.session_state.processor = None

    custom_write("Step 1: Collect images that will be used for training.", 20)
    st.markdown("""
                    In order to train a predictor in detecting the desired gesture we first have to provide the images that it will be trained on.
                    Ideally, they have to portrait the gesture in different angles and distances from the camera to improve robustness.
                
                    You can use the already existing dataset of 4 different gestures if you like (Left: 👈, Right: 👉, Up: ☝️, Down: 👇):
                """)
    
  
    if st.session_state.demo_dataset_loaded:
        st.button("Clear dataset", on_click=clear_dataset)
    else:
        st.button("Use demo dataset", on_click=use_demo_dataset)

        st.markdown("""
                        Or create your own by selecting the amount of gestures you want to be taught and the number of frames that are going to be used for each one of them.
                        Then start the camera stream and when you are ready for the model to collect the frames for each category press the corresponding button!
                    """)

        number_of_classes = st.selectbox(
            "Choose how many gestures the model is going to be trained on:",
            [i + 2 for i in range(9)]
        )
        st.session_state.number_of_classes = number_of_classes

        st.session_state.dataset_size = st.selectbox(
            "Choose how many frames are going to be used for each gesture:",
            [i for i in range(100, 300, 50)]
        )

        columns = st.columns(number_of_classes)
        for class_index in range(number_of_classes):
            with columns[class_index]:
                st.button(f"Start Capturing for Class {class_index}", on_click=start_class_capture, args=(class_index,))

        # Set up the webcam feed with image collection
        webrtc_ctx = webrtc_streamer(
            key="collect_images",
            mode=WebRtcMode.SENDRECV,
            video_processor_factory=ImageCollectorProcessor, 
            media_stream_constraints={"video": True, "audio": False},
            rtc_configuration={  # Add this config
                "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
            }
        )

        # Assign the processor instance to session state if it exists
        if webrtc_ctx.video_processor:
            st.session_state.processor = webrtc_ctx.video_processor

            os.makedirs(st.session_state.data_dir, exist_ok=True)

            # Initialize directories for each class
            for j in range(number_of_classes):
                class_dir = os.path.join(st.session_state.data_dir, str(j))
                if not os.path.exists(class_dir):
                    os.makedirs(class_dir)

