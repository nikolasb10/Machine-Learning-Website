import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
import streamlit as st
from general_utils.custom_write import custom_write
import os

# Dictionary to map classifier names to their corresponding model classes
CLASSIFIERS = {
    "Random Forest": RandomForestClassifier,
    "Decision Tree": DecisionTreeClassifier,
    "Logistic Regression": LogisticRegression
}

if "score" not in st.session_state:
    st.session_state.score = 0

def train_classifier_proc(option):
    # Load dataset
    if st.session_state.demo_dataset_loaded:
        data_folder = "./gesture_recognition_utils/train_sign_detector/demo_data"
    else:
        data_folder = st.session_state.data_dir

    data_dict = pickle.load(open(f"{data_folder}/data.pickle", 'rb'))
    data = np.asarray(data_dict['data'])
    labels = np.asarray(data_dict['labels'])

    # Split the data into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)

    # Initialize the classifier based on user's choice
    classifier_class = CLASSIFIERS.get(option)
    if classifier_class is None:
        st.error("Invalid classifier option selected.")
        return

    # # Train the selected classifier
    # with st.spinner(f"Training {option}..."):
    model = classifier_class()
    model.fit(x_train, y_train)
    y_predict = model.predict(x_test)
    st.session_state.score = accuracy_score(y_test, y_predict)
    
    with open(f'{data_folder}/model.p', 'wb') as f:
        pickle.dump({'model': model}, f)

def train_classifier():
    custom_write("Step 3: Choose and train classifier.", 20)

    # Classifier selection
    option = st.selectbox(
        "Which classifier would you like to train?",
        list(CLASSIFIERS.keys())
    )

    isTrainDisabled = not (os.path.isfile(f"{st.session_state.data_dir}/data.pickle") or st.session_state.demo_dataset_loaded)

    # Trigger training on button click
    trained = st.button("Train classifier", on_click=train_classifier_proc, args=(option,), disabled=isTrainDisabled)

    # Check if the data.pickle file exists or the demo dataset is loaded to let the user train a model
    if isTrainDisabled:
        st.write("(You need to choose the demo dataset or create a new one to train a classifier)")

    # Display accuracy and save the model
    if trained:
        st.write(f"{st.session_state.score*100}% of samples were classified correctly with {option}!")