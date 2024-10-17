import cv2
import streamlit as st
import os

def draw_gaze_direction(output_gazes, gaze_start_coords_dict, frame_batch, counter):
    """
    Draws gaze direction on each frame.

    dx, dy: The direction of the gaze (x and y components).
    gaze_start_coords_dict: A dictionary where keys are (human_id, frame_number) and values are starting coordinates (x, y).
    frame_batch: A list of frames (images) to draw the gaze direction on.
    """
    # Loop through each frame in the batch
    for frame_index, frame in enumerate(frame_batch):
        # Loop through each human's gaze data
        for human_id in range(len(output_gazes)):
            # Get the starting point (x, y) of the gaze for the current frame
            if (frame_index, human_id) in gaze_start_coords_dict:
                dx, dy = -output_gazes[human_id][0][0], -output_gazes[human_id][0][1]

                start_point = gaze_start_coords_dict[(frame_index, human_id)]
                start_point = (int(start_point[0]), int(start_point[1]))

                # print(f"Frame index: {frame_index}, Start point: {start_point}")
                # Calculate the endpoint based on the gaze direction (dx, dy)
                norm = 120
                end_point = (int(start_point[0] + dx * norm), int(start_point[1] + dy * norm))  # Scale the arrow length

                # Draw a dot at the starting point
                cv2.circle(frame, start_point, 10, (0, 0, 255), -1)  # Red dot for the starting point

                # Draw an arrow from the starting point to the direction of the gaze
                cv2.arrowedLine(frame, start_point, end_point, (0, 255, 0), 3, tipLength=0.3)  # Green arrow for gaze

        # st.image(frame, caption="Head Detection Results", use_column_width=True)
                
        # Save the frame as an image
        folder_path = f"./gaze_tracking_utils/video_frames/final_frames"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        frame_save_path = f"{folder_path}/frame_{counter+frame_index}.jpg"
        cv2.imwrite(frame_save_path, frame)

                
