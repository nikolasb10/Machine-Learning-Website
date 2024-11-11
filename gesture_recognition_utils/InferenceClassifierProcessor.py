import pickle
import cv2
import mediapipe as mp
import numpy as np
import av
from streamlit_webrtc import VideoProcessorBase

# MediaPipe setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

# Define label dictionary
labels_dict = {0: 'Up', 1: 'Left', 2: 'Right', 3: 'Down'}

class InferenceClassifierProcessor(VideoProcessorBase):
    def __init__(self, model_path):
        self.x_ = []
        self.y_ = []
        self.data_aux = []

        # Load the model
        model_dict = pickle.load(open(model_path, 'rb'))
        self.model = model_dict['model']

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        # Convert the incoming frame to a format usable by OpenCV
        img = frame.to_ndarray(format="bgr24")

        H, W, _ = img.shape

        # Convert to RGB for MediaPipe
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Process hand landmarks
        results = hands.process(img_rgb)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw the landmarks and connections
                mp_drawing.draw_landmarks(
                    img,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )

            # Reset coordinate lists for each hand
            self.x_ = []
            self.y_ = []
            self.data_aux = []

            # Process the landmarks of the hand
            for hand_landmarks in results.multi_hand_landmarks:
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    self.x_.append(x)
                    self.y_.append(y)

                # Normalize the landmarks
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    self.data_aux.append(x - min(self.x_))
                    self.data_aux.append(y - min(self.y_))

            # Predict the character based on the hand landmarks
            x1 = int(min(self.x_) * W) - 10
            y1 = int(min(self.y_) * H) - 10
            x2 = int(max(self.x_) * W) - 10
            y2 = int(max(self.y_) * H) - 10

            if len(self.data_aux) == 42:
                # Model prediction
                prediction = self.model.predict([np.asarray(self.data_aux)])
                predicted_character = labels_dict[int(prediction[0])]

                # Draw bounding box and predicted text on the image
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 0), 4)
                cv2.putText(img, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3, cv2.LINE_AA)

        # Return the processed frame
        return av.VideoFrame.from_ndarray(img, format="bgr24")

