import mediapipe as mp
import cv2
from collections import deque
import av 
import numpy as np

# Set up Mediapipe for hand detection
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Define the video processor class
class VirtualKeyboardProcessor:
    def __init__(self):
        self.last_pressed_key = None
        self.last_press_time = None
        
        # Define keyboard layout (simple 3x3 grid for demo purposes)
        self.keys = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "I"]]
        self.key_coords = {}  # To store coordinates of each key
        self.typed_text = deque(maxlen=30)  # Store last typed characters

    def recv(self, frame):
        img = cv2.flip(frame.to_ndarray(format="bgr24"), 1)  # Flip horizontally
        h, w, _ = img.shape
        
        # Detect hands
        img_rgb     = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results     = hands.process(img_rgb)
        current_key = (0, 0, 0, 0)
        pressed_key = (0, 0, 0, 0)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw landmarks
                mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Get the index and middle finger tip coordinates
                index_tip = hand_landmarks.landmark[8]
                middle_tip = hand_landmarks.landmark[12]
                
                fingertip_x, fingertip_y = int(index_tip.x * w), int(index_tip.y * h)
                middle_finger_x, middle_finger_y = int(middle_tip.x * w), int(middle_tip.y * h)
                
                # Draw the fingertips for visualization
                cv2.circle(img, (fingertip_x, fingertip_y), 8, (0, 255, 0), cv2.FILLED)
                cv2.circle(img, (middle_finger_x, middle_finger_y), 8, (255, 0, 0), cv2.FILLED)

                # Calculate distance between index and middle fingertips
                distance = np.linalg.norm(np.array([fingertip_x, fingertip_y]) - np.array([middle_finger_x, middle_finger_y]))

                # Define a threshold for "collision" (adjust this value based on testing)
                collision_threshold = 22

                # Check if fingertips are colliding (distance below threshold)
                for key, ((x1, y1), (x2, y2)) in self.key_coords.items():
                    if x1 < fingertip_x < x2 and y1 < fingertip_y < y2:
                        current_key = (x1, y1, x2, y2)
                        # Check for press duration to avoid repeated key presses
                        isTimeElapsed = (self.last_press_time is None or (cv2.getTickCount() - self.last_press_time) / cv2.getTickFrequency() > 2) # Check if enough time has passed from the last press
                        isPressedKey  = (self.last_press_time is None or (cv2.getTickCount() - self.last_press_time) / cv2.getTickFrequency() > 0.5)
                        if (distance < collision_threshold) & (key != self.last_pressed_key or isTimeElapsed):
                            pressed_key = (x1, y1, x2, y2)
                            self.typed_text.append(key)  # Register key press
                            self.last_pressed_key = key
                            self.last_press_time = cv2.getTickCount()
                        elif not isPressedKey:
                            pressed_key = (x1, y1, x2, y2)

                        break

        # Define the overlay for transparency
        overlay = img.copy()
        
        # Define keyboard layout and color settings
        key_size           = 90
        offset_x, offset_y = 100, 50
        pressed_color      = (0, 255, 0)       # Pressed color (green)
        hover_color        = (255, 80, 0)      # Hover color (light blue)
        alpha              = 0.4               # Transparency factor
        space              = 5

        # Draw keyboard layout on the overlay
        for row_idx, row in enumerate(self.keys):
            for col_idx, key in enumerate(row):
                x1, y1 = offset_x + col_idx * (key_size + space), offset_y + row_idx * (key_size + space)
                x2, y2 = x1 + key_size, y1 + key_size

                self.key_coords[key] = ((x1, y1), (x2, y2))

                key_color = (255, 0, 0)         # Normal color (blue)
                if pressed_key == (x1, y1, x2, y2):
                    key_color = pressed_color
                elif current_key == (x1, y1, x2, y2): 
                    key_color = hover_color

                # Set color based on hover state
                cv2.rectangle(overlay, (x1, y1), (x2, y2), key_color, -1)
                cv2.putText(overlay, key, (x1 + 30, y1 + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Blend overlay with the original image
        cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

        # Display typed text on the frame
        cv2.putText(img, f"Typed: {''.join(self.typed_text)}", (10, h - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        return av.VideoFrame.from_ndarray(img, format="bgr24")
