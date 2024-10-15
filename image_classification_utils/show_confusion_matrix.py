import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import numpy as np

# def show_confusion_matrix():
#     class_names = ["Elefante", "Farfalla", "Mucca", "Pecora", "Scoiattolo"]

#     # Read the CSV file
#     df = pd.read_csv('./image_classification_utils/labels_for_features.csv')

#     # Extract true_labels and predicted_labels
#     true_labels = df['true_labels'].tolist()
#     predicted_labels = df['predicted_labels'].tolist()

#     # Calculate confusion matrix
#     cm = confusion_matrix(true_labels, predicted_labels)

#     # Create a figure for the confusion matrix
#     fig, ax = plt.subplots(figsize=(6, 4))

#     # Plot the confusion matrix with Matplotlib
#     cax = ax.matshow(cm, cmap="Blues", alpha=0.5)

#     # Add colorbar
#     fig.colorbar(cax)

#     # Set axis labels
#     ax.set_xlabel('Predicted Labels', color='white')
#     ax.set_ylabel('True Labels', color='white')

#     # Set the ticks to match the class names
#     ax.set_xticks(np.arange(len(class_names)))
#     ax.set_yticks(np.arange(len(class_names)))

#     ax.set_xticklabels(class_names, color='white')
#     ax.set_yticklabels(class_names, color='white')

#     # Rotate x-tick labels
#     plt.xticks(rotation=45, ha='right')

#     # Annotate the confusion matrix
#     for i in range(len(class_names)):
#         for j in range(len(class_names)):
#             ax.text(j, i, cm[i, j], ha='center', va='center', color='black')

#     # Set title with white font
#     ax.set_title('Confusion Matrix', color='white')

#     # Set the background to be transparent
#     fig.patch.set_alpha(0)  # Make the figure background transparent
#     ax.set_facecolor('none')  # Make the axes background transparent

#     # Show the plot in Streamlit
#     st.pyplot(fig)
    # Calculate confusion matrix
    # cm = confusion_matrix(true_labels, predicted_labels)
    # print(cm)
    # # Create a heatmap for the confusion matrix
    # fig, ax = plt.subplots(figsize=(6, 4))

    # # Set the background of the plot and figure to transparent
    # fig.patch.set_alpha(0)  # Make the figure background transparent
    # ax.set_facecolor('none')  # Make the axes background transparent
    # plt.figure(figsize=(10, 8))
    # sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False, 
    #             xticklabels=class_names, yticklabels=class_names, ax=ax)
    # # Set labels and title with white font
    # ax.set_xlabel('Predicted Labels', color='white')
    # ax.set_ylabel('True Labels', color='white')
    # ax.set_title('Confusion Matrix', color='white')

    # # Set tick labels color to white
    # plt.xticks(rotation=45, ha='right', color='blue')  # X axis tick labels
    # plt.yticks(rotation=0, color='white')  # Y axis tick labels

    # # Optionally, you can also set the color of the axis spines (edges)
    # ax.spines['top'].set_color('white')
    # ax.spines['bottom'].set_color('white')
    # ax.spines['left'].set_color('white')
    # ax.spines['right'].set_color('white')

    # # Show the plot in Streamlit
    # st.pyplot(fig)

import streamlit as st
import numpy as np
import pandas as pd
import plotly.figure_factory as ff
from sklearn.metrics import confusion_matrix

def show_confusion_matrix():
    class_names = ["Elefante", "Farfalla", "Mucca", "Pecora", "Scoiattolo"]

    # Read the CSV file
    df = pd.read_csv('./image_classification_utils/labels.csv')

    # Extract true_labels and predicted_labels
    true_labels = df['true_labels'].tolist()
    predicted_labels = df['predicted_labels'].tolist()

    # Calculate confusion matrix
    cm = confusion_matrix(true_labels, predicted_labels)

    # Plot using Plotly
    fig = ff.create_annotated_heatmap(
        z=cm,
        x=class_names,
        y=class_names,
        colorscale='Blues',
        showscale=False,  # Set this to False to remove the colorbar
    )

    # Update the layout for axis labels and tick labels
    fig.update_layout(
        title='Confusion Matrix',
        title_font=dict(size=24, color='white'),
        xaxis_title='Predicted Labels',
        yaxis_title='True Labels',
        xaxis_title_font=dict(size=20, color='white'),
        yaxis_title_font=dict(size=20, color='white'),
        xaxis_tickangle=-45,  # Rotate x-axis labels for better readability
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(len(class_names))),
            ticktext=class_names,
            tickfont=dict(size=16, color='white'),  # Font size for x-axis tick labels
            side='bottom'
        ),
        yaxis=dict(
            tickmode='array',
            tickvals=list(range(len(class_names))),
            ticktext=class_names,
            tickfont=dict(size=16, color='white'),  # Font size for y-axis tick labels
            autorange='reversed'  # Reverse the order of the y-axis labels
        ),
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
        paper_bgcolor='rgba(0,0,0,0)',
        height=700  # Increase height of the matrix
    )

    # Show the plot in Streamlit
    st.plotly_chart(fig)

    return true_labels, predicted_labels, class_names