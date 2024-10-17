import numpy as np
import cv2
from detector_utils.detect_humans import detect_humans
from PIL import Image
import streamlit as st
import mediapipe as mp
import os

def crop_head_and_find_gaze_start_coords(image, x1, y1):
    # Convert image to RGB
    img_rgb = image.convert('RGB')

    # Convert to numpy array (MediaPipe works with OpenCV-like images)
    img_np = np.array(img_rgb)

    mp_face_detection = mp.solutions.face_detection
    
    # Initialize the face detection model
    with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:
        results = face_detection.process(img_np)

        # Store the eye coordinates
        gaze_start_coords = []

        # Draw bounding boxes around the face(s)
        if results.detections:
            for detection in results.detections:
                # Extract bounding box
                bboxC      = detection.location_data.relative_bounding_box
                ih, iw, _  = img_np.shape
                x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)

                # Crop head
                cropped_head = image.crop((x, y, x + w, y + h))

                # Retrieve key points (eyes, nose, mouth)
                keypoints = detection.location_data.relative_keypoints

                # Extract left and right eye coordinates
                left_eye  = keypoints[0]  # Left eye is at index 0
                right_eye = keypoints[1]  # Right eye is at index 1

                # Convert relative coordinates to absolute pixel values
                left_eye_x, left_eye_y   = int(left_eye.x * iw), int(left_eye.y * ih)
                right_eye_x, right_eye_y = int(right_eye.x * iw), int(right_eye.y * ih)

                # Store the eye coordinates
                gaze_start_coords.append(((left_eye_x + right_eye_x)/2+x1, (left_eye_y + right_eye_y)/2+y1))

                return cropped_head, gaze_start_coords
        else:
            st.write("No head detected.")
            return image, [(0,0)]

def extract_head_images(frame_batch):
    # Find the humans only for the mid frame to save time
    cv2.imwrite("./gaze_tracking_utils/temp_frame.jpg", frame_batch[3])
    _ , human_results = detect_humans("./gaze_tracking_utils/temp_frame.jpg")
    
    gaze_start_coords_dict = {}
    for idx_frame, frame in enumerate(frame_batch):
        for idx_human, box in enumerate(human_results.boxes):
            if idx_human == 2:
                idx_human = 1
                continue
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())  # Convert coordinates to integers

            # Crop the image
            original_image = Image.open("./gaze_tracking_utils/temp_frame.jpg")
            cropped_image  = original_image.crop((x1, y1, x2, y2))

            cropped_head, gaze_start_coords = crop_head_and_find_gaze_start_coords(cropped_image, x1, y1)

            # Save cropped_head
            folder_path = f"./gaze_tracking_utils/video_frames/human_{idx_human}"
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                
            save_path = f"{folder_path}/frame_{idx_frame}.jpg"
            cropped_head.save(save_path, "JPEG")

            # Save gaze start coords
            key   = (idx_frame, idx_human)  # Key as tuple of two integers
            value = gaze_start_coords[0]  # Convert the string representation of the tuple into an actual tuple

            # Store the key-value pair in the dictionary
            gaze_start_coords_dict[key] = value

    return idx_human+1, gaze_start_coords_dict
        
        