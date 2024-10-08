from ultralytics import YOLO
import cv2

def detect_humans(image_path):
    model = YOLO("./detector_utils/yolo11n.pt")
    results = model(image_path)
    # print(results[0])
    human_detections_indexes = [idx for idx, r in enumerate(results[0]) if r.boxes.cls == 0]
    result_img = results[0][human_detections_indexes].plot()

    # Convert BGR to RGB for Streamlit
    img_rgb = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
    
    return img_rgb
