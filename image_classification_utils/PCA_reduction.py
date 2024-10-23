import torch
import pandas as pd
import streamlit as st
import plotly.graph_objs as go

@st.cache_data
def PCA_reduction():
    # Read the CSV file
    df = pd.read_csv('./image_classification_utils/labels_for_features.csv')

    # Extract true_labels, predicted_labels and features
    true_labels = df['true_labels'].tolist()
    features = torch.load('./image_classification_utils/features.pt')

    # Calculate the mean and standard deviation for standardization
    mean = torch.mean(features, dim=0)
    std_dev = torch.std(features, dim=0)

    # Perform standardization by subtracting the mean and dividing by standard deviation
    scaled_data = (features - mean) / std_dev

    # Perform Singular Value Decomposition
    U, S, V = torch.svd(scaled_data)

    k = 3 # dimensions in which to reduce
    principal_components = V[:, :k]
    # print("\nSelected Principal Components:")
    # print(principal_components)

    # Projecting the original data onto the reduced dimensional space
    projected_data = torch.mm(scaled_data, principal_components)

    # get the indexes for the images of every class
    idx_0 = []
    idx_1 = []
    idx_2 = []
    idx_3 = []
    idx_4 = []
    for i in range(len(true_labels)):
        if (true_labels[i]==0):
            idx_0.append(i)
        elif (true_labels[i]==1):
            idx_1.append(i)
        elif (true_labels[i]==2):
            idx_2.append(i)
        elif (true_labels[i]==3):
            idx_3.append(i)
        else:
            idx_4.append(i)

    # Extract x, y and z coordinates
    x = projected_data[:, 0]
    y = projected_data[:, 1]
    z = projected_data[:, 2]

    classes = ["Elefante", "Farfalla", "Mucca", "Pecora", "Scoiattolo"]
    colors = ['red', 'blue', 'green', 'purple', 'orange']

    # Initialize Plotly figure
    fig = go.Figure()

    # Iterate over each group and add the 3D scatter points for the group
    for i, idx_list in enumerate([idx_0, idx_1, idx_2, idx_3, idx_4]):
        fig.add_trace(go.Scatter3d(
            x=x[idx_list],
            y=y[idx_list],
            z=z[idx_list],
            mode='markers',
            marker=dict(size=5, color=colors[i], opacity=0.8),
            name=classes[i]
        ))

    # Set layout for the plot
    fig.update_layout(
        title="PCA Reduction to 3 Dimensions",
        scene=dict(
            xaxis_title="X-axis",
            yaxis_title="Y-axis",
            zaxis_title="Z-axis"
        ),
        legend_title="Animal Classes",
        width=800,
        height=600
    )

    # Display the plot in Streamlit
    st.plotly_chart(fig)

