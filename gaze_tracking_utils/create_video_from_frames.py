import cv2
import os
import re
import moviepy.video.io.ImageSequenceClip

# Function to extract the numeric part from filenames
def extract_frame_number(filename):
    match = re.search(r'frame_(\d+)\.jpg', filename)
    return int(match.group(1)) if match else -1

def create_video_from_frames(frame_folder, output_video_path, fps=30):
    """
    Create a video from frames in a specified folder.
    
    frame_folder: Path to the folder containing frames.
    output_video_path: Path to save the output video.
    fps: Frames per second for the output video.
    """
    # Get all image files from the folder
    images = [f"{frame_folder}/{img}" for img in os.listdir(frame_folder) if img.endswith((".png", ".jpg", ".jpeg"))]
    
    # Sort the filenames based on the numeric part
    images = sorted(images, key=extract_frame_number)
    # images_full_paths = [f"{frame_folder}/{img}" for img in images]

    clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(images, fps=fps)
    clip.write_videofile(output_video_path)
    print(f"Video saved as {output_video_path}")

