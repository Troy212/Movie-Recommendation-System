import streamlit as st
import pickle
import pandas as pd
import requests


# Function to fetch poster image from TMDB API
def fetch_poster(movie_id):
    try:
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=b5f7ec1a47a072fc6e5f94c6a4857813&language=en-US',
            timeout=15
        )
        response.raise_for_status()  # Raises an error for bad responses
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            st.warning("Poster not found for this movie, displaying placeholder.")
            return "https://via.placeholder.com/150"  # Placeholder image
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        st.error(f"Request exception occurred: {req_err}")
    return "https://via.placeholder.com/150"  # Placeholder image in case of an error


# Function to recommend movies based on similarity
def recommend(movie):
    try:
        movie_index = movies[movies['title'] == movie].index[0]
    except IndexError:
        st.error("Movie not found in the dataset.")
        return [], []

    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id  # Ensure the correct movie_id is used
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters


# Load the movie data
try:
    movies_dict = pickle.load(open('movie_dict', 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except FileNotFoundError:
    st.error("Required data files are missing. Please check your setup.")
    st.stop()

st.title('Movie Recommendation System')

# Dropdown menu for movie selection
selected_movie_name = st.selectbox(
    'Select a movie',
    movies['title'].values
)

# Button to get recommendations
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    # Display recommendations with posters in columns
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        if idx < len(names):  # Ensure there are enough movies to display
            with col:
                st.text(names[idx])
                st.image(posters[idx], use_column_width=True)
