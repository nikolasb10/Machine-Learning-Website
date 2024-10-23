import numpy as np
from bokeh.plotting import figure, show
from bokeh.io import output_file
from bokeh.models import Legend, ColumnDataSource
from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import label_binarize
import streamlit as st
from bokeh.embed import components
import pandas as pd 

@st.cache_data
def ROC_curves(true_labels, predicted_labels, classes):
    # Assume you already have true_labels and predicted_labels
    n_classes = len(classes)
    
    # Binarize the labels
    y_onehot_test = label_binarize(true_labels, classes=range(n_classes))
    y_onehot_pred = label_binarize(predicted_labels, classes=range(n_classes))

    # Create a figure for ROC curves with transparent background
    p = figure(
        title="ROC Curves",
        x_axis_label='False Positive Rate',
        y_axis_label='True Positive Rate',
        width=700, height=600,
        background_fill_color=None,  # Transparent background
        border_fill_color=None,      # Transparent border
        outline_line_color="white",  # Optional: Set outline to white for better visibility
    )

    # Set title font to white
    p.title.text_color = "white"
    p.title.text_font_size = "16pt"  # Optional: Set font size of title

    # Customize the grid and axis lines for better contrast
    p.xaxis.axis_label_text_color = "white"
    p.yaxis.axis_label_text_color = "white"
    p.xaxis.major_label_orientation = "vertical"
    p.xaxis.axis_line_color = "white"
    p.yaxis.axis_line_color = "white"
    p.grid.grid_line_color = "gray"  # Grid lines for better visibility

    colors = ["blue", "green", "red", "orange", "purple"]
    legend_items = []

    for class_id in range(n_classes):
        # Calculate ROC curve and AUC for each class
        fpr, tpr, _ = roc_curve(y_onehot_test[:, class_id], y_onehot_pred[:, class_id])
        roc_auc = auc(fpr, tpr)
        
        # Create a ColumnDataSource
        source = ColumnDataSource(data={'fpr': fpr, 'tpr': tpr})

        # Add line to the plot
        line = p.line('fpr', 'tpr', source=source, line_width=2, color=colors[class_id], alpha=0.7)
        
        # Add the legend label for the current class
        legend_items.append((f"Class {classes[class_id]} (AUC = {roc_auc:.2f})", [line]))

    # Add diagonal line for reference (random classifier line)
    p.line([0, 1], [0, 1], line_dash="dashed", line_color="white", legend_label="Random Classifier")

    # Add legends
    legend = Legend(
        items=legend_items,
        background_fill_color=None,  # Transparent background for the legend
        border_line_color="white",    # Border of the legend
        label_text_font_size="12pt",  # Font size of the legend
        label_text_color="white"      # White color for legend text
    )
    p.add_layout(legend, 'right')

    # Show plot using Streamlit
    st.bokeh_chart(p, use_container_width=True)
