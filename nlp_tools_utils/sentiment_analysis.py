import streamlit as st
from general_utils.custom_write import custom_write
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer

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

def sentiment_analysis():
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