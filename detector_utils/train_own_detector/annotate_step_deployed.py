import streamlit as st
from PIL import Image, ImageDraw
import pandas as pd

### Helper Functions

def next_button_clicked():
    if st.session_state.image_index < len(st.session_state.uploaded_files) - 1:
        st.session_state.image_index += 1
        st.session_state.temp_coords = []

def previous_button_clicked():
    if st.session_state.image_index > 0:
        st.session_state.image_index -= 1
        st.session_state.temp_coords = []

def add_bounding_box(left, top, width, height):
    bounding_box = {
        "left": left,
        "top": top,
        "width": width,
        "height": height,
    }
    st.session_state.bounding_boxes[st.session_state.image_index].append(bounding_box)
    st.session_state.temp_coords = []

def delete_bbox(df_bboxes, row):
    # Remove the row from the DataFrame
    df_bboxes.drop(row, inplace=True)
    # Update session state with the new DataFrame
    st.session_state.bounding_boxes[st.session_state.image_index] = df_bboxes.to_dict(orient="records")

def add_axis_labels(img):
    """Add axis labels to the image."""
    # Create a larger canvas to fit the image and axis labels
    axis_padding = 50  # Space for the axis labels
    img_with_axis = Image.new("RGB", (img.width + axis_padding, img.height + axis_padding), "white")
    
    # Paste the image on the new canvas
    img_with_axis.paste(img, (axis_padding, axis_padding))
    draw = ImageDraw.Draw(img_with_axis)

    # Draw horizontal axis labels (top)
    for x in range(0, img.width, 50):  # Draw label every 50 pixels
        draw.text((axis_padding + x, axis_padding - 20), str(x), fill="black")

    # Draw vertical axis labels (left)
    for y in range(0, img.height, 50):  # Draw label every 50 pixels
        draw.text((axis_padding - 30, axis_padding + y), str(y), fill="black")
    
    return img_with_axis

def annotate_step():
    st.write("Annotate images with bounding boxes")
    uploaded_files = st.session_state.uploaded_files

    if uploaded_files:
        # Initialize bounding boxes state if not already set
        if 'bounding_boxes' not in st.session_state:
            st.session_state.bounding_boxes = [[] for _ in range(len(uploaded_files))]
            st.session_state.temp_coords = []

        current_image_index = st.session_state.image_index
        total_images = len(uploaded_files)
        current_image = uploaded_files[current_image_index]
                # Create layout with two columns: left for image, right for buttons
        img_col, btn_col = st.columns([3, 2])  # Adjust proportions as needed

        with img_col:
            img = Image.open(current_image)

            # Resize image
            max_display_width = 500  # Adjust width as needed
            aspect_ratio = img.height / img.width
            img_resized = img.resize((max_display_width, int(max_display_width * aspect_ratio)))

            # Draw existing bounding boxes for the current image
            img_draw = img_resized.copy()
            draw = ImageDraw.Draw(img_draw)
            for bbox in st.session_state.bounding_boxes[current_image_index]:
                draw.rectangle(
                    [bbox["left"], bbox["top"], bbox["left"] + bbox["width"], bbox["top"] + bbox["height"]],
                    outline="red",
                    width=3
                )
            
            # Add axis labels
            img_with_axis = add_axis_labels(img_draw)

            st.image(img_with_axis, caption=f"Image {current_image_index + 1} of {total_images}", use_column_width=False)


        with btn_col:
            # Display progress
            st.write(f"Progress: Image {current_image_index + 1} of {total_images}")

            # Navigation buttons
            col1, col2 = st.columns(2)  # Adjust proportions as needed
            with col1:
                st.button("Previous Image", on_click=previous_button_clicked, disabled=current_image_index == 0)
            with col2:
                st.button("Next Image", on_click=next_button_clicked, disabled=current_image_index == total_images - 1)
            
            # Capture bounding box coordinates manually
            st.write("Enter bounding box coordinates:")
            col1, col2 = st.columns(2)  # Adjust proportions as needed
            with col1:
                left = st.number_input("Left", min_value=0, max_value=img_resized.width)
                width = st.number_input("Width", min_value=0, max_value=img_resized.width)
            with col2:
                top = st.number_input("Top", min_value=0, max_value=img_resized.height)
                height = st.number_input("Height", min_value=0, max_value=img_resized.height)

            st.button("Add bounding box", on_click=add_bounding_box, args=(left, top, width, height))

            # Display bounding boxes in table format
            if st.session_state.bounding_boxes[current_image_index]:
                df_bboxes = pd.DataFrame(st.session_state.bounding_boxes[current_image_index])
                st.table(df_bboxes)

                option = st.selectbox("Select bounding box to delete:", options=(i for i in df_bboxes.iterrows()))
                st.button("Delete bounding box", on_click=delete_bbox, args=(df_bboxes, option))

    else:
        st.write("Please provide images to annotate.")

