import os
import cv2
from streamlit_webrtc import VideoProcessorBase
import streamlit as st
import av

DATA_DIR = './gesture_recognition_utils/train_sign_detector/data_directory'

class ImageCollectorProcessor(VideoProcessorBase):
    def __init__(self):
        self.current_class = -1
        self.frame_counter = 0
        self.capturing     = False  # Flag to start/stop capturing
        self.dataset_size  = 200

    def start_capture(self, class_index, dataset_size):
        self.current_class = class_index
        self.frame_counter = 0
        self.capturing     = True
        self.dataset_size  = dataset_size

    def stop_capture(self):
        self.capturing = False
        st.write(f"Data collection for class {self.current_class} completed.")

    def recv(self, frame):

        img = frame.to_ndarray(format="bgr24")

        # Display "Ready?" text overlay
        if not self.capturing:
            cv2.putText(img, 'Ready? Press "Start" to capture!', (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2, cv2.LINE_AA)

        # Capture and save frames if capturing flag is set
        if self.capturing and self.frame_counter < self.dataset_size:
            class_dir = os.path.join(DATA_DIR, str(self.current_class))
            filename = os.path.join(class_dir, f"{self.frame_counter}.jpg")
            cv2.imwrite(filename, img)  # Save frame to the correct class directory

            # Increment frame counter
            self.frame_counter += 1
            cv2.putText(img, f"Capturing Class {self.current_class} - Image {self.frame_counter}/{self.dataset_size}", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)

            # Stop capturing if dataset size is reached
            if self.frame_counter >= self.dataset_size:
                self.stop_capture()

        return av.VideoFrame.from_ndarray(img, format="bgr24")
