import cv2
from gaze_tracking_utils.extract_head_images import extract_head_images
import torch
from .Gaze360Model import GazeLSTM
from .get_gaze_direction import get_gaze_direction
from .draw_gaze_direction import draw_gaze_direction
from .create_video_from_frames import create_video_from_frames
import streamlit as st

def modify_state_dict(state_dict):
    # Modify the keys of the state_dict to remove 'module.' prefix
    new_state_dict = {}

    for k, v in state_dict.items():
        # Remove 'module.' from key names if present
        if k.startswith('module.'):
            new_state_dict[k[7:]] = v  # remove 'module.' prefix
        else:
            new_state_dict[k] = v
    return new_state_dict

# Add frames of a video in its folder starting and ending on a specific frame
def create_video_with_gaze_directions(output_dir, video_path, start_frame=0, end_frame=1, progress=True):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return

    # Get the total number of frames in the video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Total frames in video: {total_frames}")

    start_frame = int(start_frame)
    end_frame   = int(end_frame)

    # Adjust end_frame if it is beyond the total number of frames
    if end_frame >= total_frames:
        end_frame = total_frames - 1

    # Set the starting frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    # Initialize the model
    model = GazeLSTM()
    # Load the checkpoint
    checkpoint = torch.load('./gaze_tracking_utils/gaze360_model.pth.tar', map_location=torch.device('cpu'))

    # Modify the keys of the state_dict to remove 'module.' prefix
    new_state_dict = modify_state_dict(checkpoint['state_dict'])

    # Load the modified state_dict into the model
    model.load_state_dict(new_state_dict)
    model.eval()

    # Progress bar initialization
    if progress:
        progress_bar     = st.progress(0)  # Initialize progress bar
        progress_text    = st.empty()

    # We iterate over the frames with a step of 7, as we are going to keep constant the gaze direction for every 7 frames
    frame_batch      = []  # List to hold 7 frames
    frames_processed = 0
    number_of_humans = 0   # Number of humans detected in frames
    while frames_processed <= end_frame:
        ret, frame = cap.read()
        
        if not ret:
            print("End of video reached.")
            break
        
        frame_batch.append(frame)
        if progress:
            # Update the progress bar
            progress_percentage = (frames_processed + 1) / (total_frames + total_frames//10)
            progress_bar.progress(progress_percentage)
            progress_text.text(f"Progress: {int(progress_percentage * 100)}%")

        # If we have collected 7 frames, process them
        if len(frame_batch) % 7 == 0:
            # Save the head images for each human existing in the 7 frames, into the folders video_frames/human_i/
            number_of_humans, gaze_start_coords_dict = extract_head_images(frame_batch)

            # Get the gaze direction for the 7 frames
            output_gazes = get_gaze_direction(model, number_of_humans)
            # print(output_gazes)

            # Draw the gaze direction in the 7 frames
            draw_gaze_direction(output_gazes, gaze_start_coords_dict, frame_batch, frames_processed-5)
            frame_batch = []  # Reset batch after processing

        frames_processed +=1
    
    cap.release()
            
    # Final update for the progress bar to 100%
    if progress:
        # Create the video with all the frames
        # Get the frame rate (FPS) using CAP_PROP_FPS property
        output_video_path = f"./gaze_tracking_utils/final_video_with_gaze_direction.mp4"
        create_video_from_frames(f"./gaze_tracking_utils/video_frames/final_frames/", output_video_path, 25)

        progress_bar.progress(1.0)
        st.success("Video processing complete!")

    return number_of_humans