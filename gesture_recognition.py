import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from gesture_recognition_utils.HandRecognitionProcessor import HandRecognitionProcessor
from general_utils.custom_write import custom_write
import platform 
import os 

def app():
    st.title("✋ Gesture Recognition")

    # Create tabs
    tabs = st.tabs(["🔊 Volume Control"])

    # Human Detector Tab
    with tabs[0]:
        custom_write("Volume Control with Gestures!",25)

        st.write("In this tab you can increase or decrease the system's volume by moving your thumb and index fingers as far as possible \
                     to increase and touching them to decrease. Put some music on to notice the differences better! (Works only on windows for now)")

        current_os = platform.system()
        st.write(f"Here {current_os}")
        os.system(f"osascript -e 'set volume output volume 60'")
        
        # Set up the webcam feed with the hand recognition processor
        webrtc_streamer(
            key="hand-recognition",
            mode=WebRtcMode.SENDRECV,
            video_processor_factory=HandRecognitionProcessor,
            media_stream_constraints={"video": True, "audio": False},
        )

