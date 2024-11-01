import streamlit as st
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from nltk.corpus import stopwords
import string
import fitz  # PyMuPDF
import requests
import toml
from general_utils.custom_write import custom_write

# Load the TOML file
config = toml.load("./.streamlit/secrets.toml")

# Access the API key
huggingface_api_key = config["api_keys"]["HUGGINGFACE_API_KEY"]

# Download VADER lexicon
nltk.download('vader_lexicon')
# nltk.download('stopwords')

# Initialize VADER sentiment analyzer
vader_analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment_textblob(text):
    """Analyze sentiment using TextBlob."""
    blob = TextBlob(text)
    return blob.sentiment.polarity, blob.sentiment.subjectivity

def analyze_sentiment_vader(text):
    """Analyze sentiment using VADER."""
    scores = vader_analyzer.polarity_scores(text)
    return scores['compound'], scores['pos'], scores['neg'], scores['neu']

def preprocess_text(text):
    # Lowercase the text
    text = text.lower()
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Tokenize the text
    tokens = text.split()
    # Remove stopwords
    tokens = [word for word in tokens if word not in stopwords.words('english')]
    return ' '.join(tokens)

def extract_text_from_pdf(pdf_file):
    # Open the PDF file
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    # Loop through each page and extract text
    for page_num in range(doc.page_count):
        page = doc[page_num]
        text += page.get_text()
    return text

def summarize_text_hf_api(text, max_length, min_length):
    headers = {"Authorization": f"Bearer {huggingface_api_key}"}
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"  # Or another summarization model
    payload = {
                "inputs": text,
                "parameters": {
                "max_length": max_length,
                "min_length": min_length
            }}
    response = requests.post(API_URL, headers=headers, json=payload)
    summary = response.json()

    return summary

def clean_and_split_text(text, max_segment_length=900):
    # Remove special characters and split text into smaller segments
    cleaned_text = text.replace("", "").replace("\n", " ")
    segments = [cleaned_text[i:i + max_segment_length] for i in range(0, len(cleaned_text), max_segment_length)]
    return segments

def app():
    st.title("💬 NLP Tools")
    # Create tabs
    tabs = st.tabs(["Sentence sentiment analysis", "Summarization Model"])

    # Human Detector Tab
    with tabs[0]:
        custom_write("😀 Sentiment Analysis", 25)
        # User input
        user_input = st.text_area("Enter text for sentiment analysis:")
        model_choice = st.selectbox("Choose sentiment analysis model:", ["TextBlob", "VADER"])

        # Analyze button
        if st.button("Analyze"):
            if user_input:
                if model_choice == "TextBlob":
                    polarity, subjectivity = analyze_sentiment_textblob(user_input)
                    st.write("**Polarity:**", polarity)
                    st.write("**Subjectivity:**", subjectivity)
                    
                    # Display sentiment result
                    if polarity > 0:
                        st.success("The sentiment is Positive! 😀")
                    elif polarity < 0:
                        st.error("The sentiment is Negative! 😢")
                    else:
                        st.warning("The sentiment is Neutral! 😐")
                elif model_choice == "VADER":
                    compound, pos, neg, neu = analyze_sentiment_vader(user_input)
                    st.write("**Compound Score:**", compound)
                    st.write("**Positive Score:**", pos)
                    st.write("**Negative Score:**", neg)
                    st.write("**Neutral Score:**", neu)
                    
                    # Display sentiment result
                    if compound > 0.05:
                        st.success("The sentiment is Positive! 😀")
                    elif compound < -0.05:
                        st.error("The sentiment is Negative! 😢")
                    else:
                        st.warning("The sentiment is Neutral! 😐")
            else:
                st.warning("Please enter some text to analyze.")
    with tabs[1]:
        # Streamlit page configuration
        custom_write("📝Text Summarization", 25)

        st.write("Choose an input method for summarization.")

        # Toggle between text input and file upload
        input_method = st.radio("Select input method:", ["Text Input", "File Upload"])

        if input_method == "Text Input":
            # Text input area
            pdf_text = st.text_area("Enter text for summarization:")
            
            # Button to summarize extracted text
            if st.button("Summarize Text"):
                st.subheader("Summary")
                if pdf_text:
                    summary = summarize_text_hf_api(pdf_text, max_length=150, min_length=30)
                    if "error" in summary:
                        st.write("There was an error with the text input, please try again!")
                        print(summary)
                    else:
                        st.write(summary[0]["summary_text"])
                else:
                    st.warning("Please enter some text to summarize.")

        elif input_method == "File Upload":
            # Upload PDF file
            uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

            if uploaded_file is not None:
                # Extract text from the PDF file
                pdf_text = extract_text_from_pdf(uploaded_file)

                # Display extracted text (optional)
                st.subheader("Extracted Text")
                st.write(pdf_text[:1000] + "...")  # Show a snippet of the text for preview

                # Button to summarize extracted text
                if st.button("Summarize PDF Text"):
                    st.subheader("Summary")
                    segments = clean_and_split_text(pdf_text)  # Assume this function cleans and splits the text
                    total_segments = len(segments)

                    progress_bar = st.progress(0)  # Initialize progress bar

                    summaries = []  # Store summaries here
                    for i, segment in enumerate(segments):
                        summary = summarize_text_hf_api(segment, max_length=150, min_length=30)

                        # Update progress
                        progress = (i + 1) / total_segments
                        progress_bar.progress(progress)

                        if "error" in summary:
                            st.write("There was an error with the text or the PDF file, try a different one!")
                            print(summary)
                            break  # Stop further processing if there's an error
                        else:
                            summaries.append(summary[0]["summary_text"])

                    # Display all summaries after processing
                    for summary in summaries:
                        st.write(summary)

                

