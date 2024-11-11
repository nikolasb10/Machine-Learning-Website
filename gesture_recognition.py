import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from gesture_recognition_utils.HandRecognitionProcessor import HandRecognitionProcessor
from gesture_recognition_utils.VirtualKeyboardProcessor import VirtualKeyboardProcessor
from gesture_recognition_utils.train_sign_detector.train_sign_detector import train_sign_detector
from general_utils.custom_write import custom_write

def app():
    st.title("✋ Gesture Recognition")

    # Create tabs
    tabs = st.tabs(["⌨️ Virtual Keyboard", "🔊 Volume Control", "👌 Train sign detector"])

    # Virtual Keyboard Tab
    with tabs[0]:
        custom_write("Type using your camera!",25)
        st.write("Hover over the virtual keyboard with your index finger and press a key by touching the tips of the index and middle fingers together. The typed text will appear below.")
        st.write("The webrtc_streamer function by streamlit currently has some issues, so there might occur some refreshes before the video feed works.")
        
        webrtc_streamer(
            key="gesture-keyboard",
            mode=WebRtcMode.SENDRECV,
            video_processor_factory=VirtualKeyboardProcessor,
            media_stream_constraints={"video": True, "audio": False},
            rtc_configuration={  # Add this config
                "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
            }
        )

    # Volume control tab
    with tabs[1]:
        custom_write("Volume Control with Gestures!",25)

        st.write("In this tab you can increase or decrease the system's volume by moving your thumb and index fingers as far as possible \
                     to increase and touching them to decrease. Put some music on to notice the differences better! (Works only on windows for now)")
        
        st.write("For now even though the detections are correct, we can't change the systems volume from the deployed app")

        # Set up the webcam feed with the hand recognition processor
        webrtc_streamer(
            key="hand-recognition",
            mode=WebRtcMode.SENDRECV,
            video_processor_factory=HandRecognitionProcessor,
            media_stream_constraints={"video": True, "audio": False},
            rtc_configuration={  # Add this config
                "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
            }
        )

    # Train sign detector tab
    with tabs[2]:
        train_sign_detector()
        

