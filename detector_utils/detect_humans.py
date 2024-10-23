from ultralytics import YOLO
import cv2
import streamlit as st

@st.cache_resource
def load_model():
    model = YOLO("./detector_utils/yolo11n.pt")
    return model 

def detect_humans(image_path):
    model   = load_model()
    results = model(image_path)
    # print(results[0])
    human_detections_indexes = [idx for idx, r in enumerate(results[0]) if r.boxes.cls == 0]
    human_results            = results[0][human_detections_indexes]
    result_img               = human_results.plot()

    # Convert BGR to RGB for Streamlit
    img_rgb = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
    
    return img_rgb, human_results
