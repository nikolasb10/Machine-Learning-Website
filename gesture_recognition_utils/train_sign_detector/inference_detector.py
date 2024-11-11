from gesture_recognition_utils.InferenceClassifierProcessor import InferenceClassifierProcessor
import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from general_utils.custom_write import custom_write
import os
from functools import partial

def inference_detector():
    custom_write("Step 4: Test the model.", 20)

    st.markdown("""
                    Use the camera stream below to test the trained gesture recognition model on your own!
                """)

    model_path = f"{st.session_state.data_dir}/model.p"
    if st.session_state.demo_dataset_loaded or os.path.isfile(f"{st.session_state.data_dir}/model.p"):
        if st.session_state.demo_dataset_loaded:
            model_path = f"./gesture_recognition_utils/train_sign_detector/demo_data/model.p"

        webrtc_streamer(
            key="inference_classifier",
            mode=WebRtcMode.SENDRECV,
            video_processor_factory=partial(InferenceClassifierProcessor, model_path),
            media_stream_constraints={"video": True, "audio": False},
            rtc_configuration={  # Add this config
                "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
            }
        )
    else:
        st.write("Train your own model or choose to use the demo dataset to inference the already trained model")