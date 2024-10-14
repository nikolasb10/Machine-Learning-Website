import numpy as np
import cv2
from detector_utils.detect_humans import detect_humans
from PIL import Image
import streamlit as st
import mediapipe as mp

def crop_head_and_find_gaze_start_coords(image, idx_frame, gaze_start_coords_dict):
    # Convert image to RGB
    img_rgb = image.convert('RGB')

    # Convert to numpy array (MediaPipe works with OpenCV-like images)
    img_np = np.array(img_rgb)

    mp_face_detection = mp.solutions.face_detection
    
    # Initialize the face detection model
    with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:
        results = face_detection.process(img_np)

        # Draw bounding boxes around the face(s)
        if results.detections:
            for idx_human, detection in enumerate(results.detections):
                print(idx_human)
                # Extract bounding box
                bboxC      = detection.location_data.relative_bounding_box
                ih, iw, _  = img_np.shape
                x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)

                # Crop head
                cropped_head = image.crop((x, y, x + w, y + h))

                # Save cropped_head
                save_path = f"./gaze_tracking_utils/video_frames/human_{idx_human}/frame_{idx_frame}.jpg"
                cropped_head.save(save_path, "JPEG")

                # Retrieve key points (eyes, nose, mouth)
                keypoints = detection.location_data.relative_keypoints

                # Extract left and right eye coordinates
                left_eye  = keypoints[0]  # Left eye is at index 0
                right_eye = keypoints[1]  # Right eye is at index 1

                # Convert relative coordinates to absolute pixel values
                left_eye_x, left_eye_y   = int(left_eye.x * iw), int(left_eye.y * ih)
                right_eye_x, right_eye_y = int(right_eye.x * iw), int(right_eye.y * ih)

                # Store the eye coordinates
                key   = (idx_frame, idx_human)  # Key as tuple of two integers
                value = ((left_eye_x + right_eye_x)/2, (left_eye_y + right_eye_y)/2) # Convert the string representation of the tuple into an actual tuple

                # Store the key-value pair in the dictionary
                gaze_start_coords_dict[key] = value
                return idx_human, gaze_start_coords_dict
        else:
            st.write("No head detected.")
            return image, [(0,0)]

def extract_head_images(frame_batch):    
    gaze_start_coords_dict = {}
    for idx_frame, frame in enumerate(frame_batch):
        cv2.imwrite("./gaze_tracking_utils/temp_frame.jpg", frame)
        original_image = Image.open("./gaze_tracking_utils/temp_frame.jpg")
        idx_human, gaze_start_coords_dict = crop_head_and_find_gaze_start_coords(original_image, idx_frame, gaze_start_coords_dict)

    return idx_human+1, gaze_start_coords_dict
        
        