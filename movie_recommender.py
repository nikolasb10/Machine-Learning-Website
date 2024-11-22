import streamlit as st
import requests
from movie_recommender_utils.get_df_data import get_df_data
from movie_recommender_utils.get_recommendations import get_recommendations
import matplotlib.pyplot as plt
import seaborn as sns

def display_similarity_heatmap(cosine_sim):
    # Set up a matplotlib figure
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Create a heatmap using Seaborn
    sns.heatmap(cosine_sim[:15, :15], cmap="YlGnBu", ax=ax)  # Show a subset for readability

    # Add labels and title
    ax.set_title("Cosine Similarity between Movies")
    ax.set_xlabel("Movie Index")
    ax.set_ylabel("Movie Index")
    
    # Display the figure in Streamlit
    st.pyplot(fig)

def get_movie_poster(movie_name, api_key):
    # TMDb API endpoint for movie search
    search_url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_name}'
    response = requests.get(search_url)
    data = response.json()
    
    if 'results' in data and len(data['results']) > 0:
        # Get the first movie result
        movie = data['results'][0]
        print(movie)

        poster_path = movie.get('poster_path', '')
        
        if poster_path:
            # Construct the full URL for the movie poster
            poster_url = f'https://image.tmdb.org/t/p/w500{poster_path}'
            return poster_url
        else:
            return None
    else:
        return None


def app():
    # Header
    st.title("🎥 Movie Recommender")
    st.write("Find movies tailored to your tastes and preferences!")

    df, indices, cosine_sim = get_df_data()
    # st.title("Cosine Similarity Heatmap")
    # display_similarity_heatmap(cosine_sim)

    # Sample data (e.g., list of movies, names, etc.)
    movies = df["movie_title"].unique()

    selected_movie = st.selectbox(
        "",
        movies,
        index=None,
        placeholder="Select a movie...",
    )
    
    if selected_movie is not None:
        recommendations = get_recommendations(df, indices, selected_movie, cosine_sim)

        # Display each recommended movie in a visually appealing way
        for _ , row in recommendations.iterrows():
            # Create a container for each movie
            with st.container():
                # Create a two-column layout for each movie
                col1, col2 = st.columns([1, 4])

                # Add an image in the first column (if you have movie posters or images)
                with col1:
                    # Replace 'YOUR_API_KEY' with your actual API key from TMDb
                    api_key = '15d2ea6d0dc1d476efbca3eba2b9bbfb'
                    poster_url = get_movie_poster(row['movie_title'], api_key)

                    if poster_url:
                        # Display the movie poster image
                        st.image(poster_url)
                    else:
                        st.image('./movie_image.jpg', width=100)  # Replace with the correct path or image URL

                # Display movie details in the second column
                with col2:
                    st.markdown(f"### {row['movie_title']}")  # Movie Title in bold
                    genres = ", ".join(row['genres'])
                    st.write(f"**Genres**: {genres}")
                    st.write(f"**Director**: {row['director_name']}")
                    st.write(f"**Cast**: {row['actor_1_name']}, {row['actor_2_name']}, {row['actor_3_name']}")

                # Add a separator between movies
                st.markdown("---")          




