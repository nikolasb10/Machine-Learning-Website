import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

# Function that creates a string consisted of specific columns for the row given
def create_soup(x):
    return ' '.join(x['plot_keywords']) + ' ' + x['actor_1_name'] + ' ' + x['actor_2_name'] + ' ' + x['actor_3_name'] + ' ' + x['director_name'] + ' ' + ' '.join(x['genres']) #+ ' ' + x['country']

# Function to convert string of categories to a list
def split_row_items(items_string):
    return [item.strip() for item in items_string.split('|')]

# Function to convert all strings to lower case and strip names of spaces
def clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ''

@st.cache_data
def get_df_data():
    # Read the CSV file into a DataFrame
    file_path = './movie_recommender_utils/movies_metadata.csv' 
    df = pd.read_csv(file_path)

    shorted_df = df[["movie_title", "budget", "plot_keywords", "genres", "popularity", "country", "director_name", "actor_1_name", "actor_2_name", "actor_3_name", "vote_average", "num_voted_users"]]

    # For each column with multiple items in each row, create a list of strings for each row inset
    columns = ['genres', 'plot_keywords']
    for column in columns:
        shorted_df[column] = shorted_df[column].fillna('')
        shorted_df[column] = shorted_df[column].apply(split_row_items)
        output_df          = shorted_df.copy()

    # Apply clean_data function to selected columns.
    columns = ['country', 'plot_keywords', 'director_name', 'genres', 'actor_1_name', 'actor_2_name', 'actor_3_name']
    for column in columns:
        shorted_df[column] = shorted_df[column].apply(clean_data)

    # Construct a reverse map of indices and movie titles
    indices = pd.Series(shorted_df.index, index=shorted_df['movie_title']).drop_duplicates()

    # Create the count matrix
    shorted_df['soup'] = shorted_df.apply(create_soup, axis=1) 
    count              = CountVectorizer(stop_words='english')
    count_matrix       = count.fit_transform(shorted_df['soup'])

    # Compute the Cosine Similarity matrix based on the count_matrix
    cosine_sim = cosine_similarity(count_matrix, count_matrix)

    return output_df, indices, cosine_sim