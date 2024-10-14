import streamlit as st
from moviepy.video.io.VideoFileClip import VideoFileClip
import cv2
from gaze_tracking_utils.create_video_with_gaze_directions import create_video_with_gaze_directions
from gaze_tracking_utils.create_video_from_frames import create_video_from_frames

def count_frames(video_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if the video file is opened successfully
    if not cap.isOpened():
        print("Error opening video file")
        return

    # Get the total number of frames in the video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Release the video capture object
    cap.release()

    return total_frames

def app():    
    # Title of the contact page
    st.title("👀 Gaze Tracker")
    st.write("In this page we utilize the Gaze360 model to track the gaze of humans in a given video! \n Below you can see a video of the resulting gazes on a short snippet!")
    total_frames = count_frames("./gaze_tracking_utils/output_video.mp4")
    output_video_path = f"./gaze_tracking_utils/final_video_with_gaze_direction.mp4"
    st.video(output_video_path)  

    st.write("If you want to go throught the process, of calculating the gaze directions press the button below!")

    go_through_proc = st.button("Go through the process")

    if go_through_proc:
        create_video_with_gaze_directions(output_dir="./gaze_tracking_utils/video_frames", video_path="./gaze_tracking_utils/output_video.mp4", start_frame=0, end_frame=2)
        st.video(output_video_path)  


        