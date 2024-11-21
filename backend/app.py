from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/movies', methods=['GET'])
def movies():
    movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    return jsonify(movies.values.tolist()), 200

def fetch_poster(movie_id):
    # url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=b5f7ec1a47a072fc6e5f94c6a4857813&language=en-US'
    # response = requests.get(url, timeout=15)
    # response.raise_for_status()
    # data = response.json()
    # poster_path = data.get('poster_path')
    # if poster_path:
    #     return "https://image.tmdb.org/t/p/w500/" + poster_path
    # else:
    return "https://placehold.co/150"

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    movie = data.get('searchQuery')
    if not movie:
        return jsonify({"error": "No movie title provided"}), 400
    
    try:
        movie_index = movies[movies['title'] == movie].index[0]
    except IndexError:
        return jsonify({"error": "Movie not found in the dataset"}), 404

    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        title = movies.iloc[i[0]].title
        poster = fetch_poster(movie_id)
        recommended_movies.append({"title": title, "poster": poster})

    return jsonify(recommended_movies), 200

if __name__ == '__main__':
    app.run(debug=True)
