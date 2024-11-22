import streamlit as st
from nlp_tools_utils.sentiment_analysis import sentiment_analysis
from nlp_tools_utils.text_summarization import text_summarization
from nlp_tools_utils.chatbot import chatbot

def app():
    st.title("💬 NLP Tools")
    # Create tabs
    tabs = st.tabs(["Sentence sentiment analysis", "Summarization Model", "Chatbot"])

    # Human Detector Tab
    with tabs[0]:
        sentiment_analysis()
    with tabs[1]:
        text_summarization()
    with tabs[2]:
        chatbot()   

