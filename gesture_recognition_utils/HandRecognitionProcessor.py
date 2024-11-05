from streamlit_webrtc import  VideoProcessorBase
import av
import cv2
import mediapipe as mp
import numpy as np
import os
import platform
import streamlit as st

# Mediapipe setup for hand recognition
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Define the video processor class
class HandRecognitionProcessor(VideoProcessorBase):
    def __init__(self):
        # Initialize audio interface once
        st.write(f"Here before")
        self.current_os = platform.system()
        self.volume_control = None
        self.volume = 40
        st.write(f"Here: {self.current_os}")
        if self.current_os == "Windows":
            st.write("Here1")
            from ctypes import cast, POINTER
            import pythoncom
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            from comtypes import CLSCTX_ALL
            
            pythoncom.CoInitialize()
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            self.volume_control = cast(interface, POINTER(IAudioEndpointVolume))
                          
    def set_system_volume(self, volume):
        # Set volume level (0.0 to 1.0)
        st.write("system_volume")
        if self.current_os == "Windows":
            self.volume_control.SetMasterVolumeLevelScalar(volume / 100.0, None)
        elif self.current_os == "Darwin":  # macOS
            os.system(f"osascript -e 'set volume output volume {volume}'")
        elif self.current_os == "Linux":  # Linux (requires `amixer`)
            os.system(f"amixer -D pulse sset Master {volume}%")

    def recv(self, frame):
        # Convert frame to BGR image (OpenCV format)
        img = frame.to_ndarray(format="bgr24")
        
        # Process the image and detect hands
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)
        st.write("Here2")
        
        # Draw hand landmarks and calculate distances if hands are detected
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw the landmarks on the image
                st.write("Here3")
                mp_drawing.draw_landmarks(
                    img, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
                )

                # Get coordinates of thumb tip (landmark 4) and index finger tip (landmark 8)
                thumb_tip = hand_landmarks.landmark[4]
                index_tip = hand_landmarks.landmark[8]
                wrist = hand_landmarks.landmark[0]
                middle_finger_base = hand_landmarks.landmark[9]
                
                # Convert normalized coordinates to pixel coordinates
                h, w, _ = img.shape
                thumb_tip_coords = (int(thumb_tip.x * w), int(thumb_tip.y * h))
                index_tip_coords = (int(index_tip.x * w), int(index_tip.y * h))
                wrist_coords = (int(wrist.x * w), int(wrist.y * h))
                middle_finger_base_coords = (int(middle_finger_base.x * w), int(middle_finger_base.y * h))
                
                # Calculate the Euclidean distance between thumb tip and index finger tip
                raw_distance = np.linalg.norm(np.array(thumb_tip_coords) - np.array(index_tip_coords))
                
                # Calculate the reference distance (wrist to middle finger base)
                reference_distance = np.linalg.norm(np.array(wrist_coords) - np.array(middle_finger_base_coords))
                
                # Normalize the thumb-index distance by the reference distance
                if reference_distance > 0:  # Avoid division by zero
                    normalized_distance = raw_distance / reference_distance
                else:
                    normalized_distance = 0

                min_distance, max_distance = 0.2, 1.4
                if normalized_distance > max_distance or normalized_distance < min_distance:
                    points_color = (0, 255, 0)        

                    # Adjust volume
                    if normalized_distance < min_distance:
                        self.volume = max(0, self.volume - 1)
                    else:
                        self.volume = min(100, self.volume + 1)

                    self.set_system_volume(self.volume)  # Adjust the system volume

                else:
                    points_color = (255, 0, 150)

                # Draw the thumb, index finger, and center of the line between them
                center_of_line = ((thumb_tip_coords[0] + index_tip_coords[0]) // 2, 
                                  (thumb_tip_coords[1] + index_tip_coords[1]) // 2)
                cv2.circle(img, thumb_tip_coords, 8, points_color, cv2.FILLED)
                cv2.circle(img, index_tip_coords, 8, points_color, cv2.FILLED)
                cv2.circle(img, center_of_line, 8, points_color, cv2.FILLED)
                cv2.line(img, thumb_tip_coords, index_tip_coords, points_color, 2)

                # Display the normalized distance and volume on the image
                cv2.putText(
                    img,
                    f"Normalized Distance: {normalized_distance:.2f}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    2,
                    cv2.LINE_AA
                )
                cv2.putText(
                    img,
                    f"Volume: {int(self.volume)}%",
                    (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    2,
                    cv2.LINE_AA
                )
        
        # Return the processed frame
        return av.VideoFrame.from_ndarray(img, format="bgr24")
