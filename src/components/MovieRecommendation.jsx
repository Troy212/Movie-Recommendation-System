// MovieRecommendation.jsx

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './picture.css';



function MovieRecommendation() {
  const [movies, setMovies] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [recommendations, setRecommendations] = useState([]);

  useEffect(() => {
    axios
      .get('http://localhost:5173/movies')
      .then((response) => setMovies(response.data))
      .catch((error) => console.error('Error fetching movie list:', error));
  }, []);

  const recommends = () => {
    axios
      .post(
        'http://localhost:5173/recommend',
        { searchQuery },
        {
          headers: {
            'Content-Type': 'application/json',
          },
        }
      )
      .then((response) => {
        setRecommendations(response.data);
        console.log(response.data);
      })
      .catch((error) =>
        console.error('Error fetching movie recommendations:', error)
      );
  };

  const filteredMovies = movies
    .filter((movie) =>
      movie[1].toLowerCase().includes(searchQuery.toLowerCase())
    )
    .slice(0, 5);

  const handleSelectMovie = (movieName) => {
    setSearchQuery(movieName);
    setShowSuggestions(false);
  };

  return (
    <div className="movie-container"> {/* Apply the background image class here */}
      <div className="container mt-5 p-4 border rounded shadow-lg" style={{ maxWidth: '500px' }}>
        <h1 className="text-center mb-4">Movie Recommendation</h1>

        <div className="mb-3 position-relative">
          <label htmlFor="movie-search" className="form-label">
            Search Movies:
          </label>
          <input
            type="text"
            id="movie-search"
            placeholder="Type to search..."
            value={searchQuery}
            className="form-control"
            onChange={(e) => {
              setSearchQuery(e.target.value);
              setShowSuggestions(true);
            }}
            onBlur={() => setTimeout(() => setShowSuggestions(false), 100)}
            onFocus={() => setShowSuggestions(true)}
          />

          {showSuggestions && searchQuery && (
            <div className="position-absolute bg-white border rounded w-100 mt-1 shadow-sm">
              {filteredMovies.map((movie, index) => (
                <div
                  key={index}
                  onMouseDown={() => handleSelectMovie(movie[1])}
                  className="p-2 hover-bg-light cursor-pointer"
                >
                  {movie[1]}
                </div>
              ))}
            </div>
          )}
        </div>

        <button
          onClick={recommends}
          className="btn btn-primary w-100 mb-4"
        >
          Search
        </button>

        {recommendations.length > 0 && (
          <div>
            <h3>Recommendations:</h3>
            <ul className="list-unstyled mt-3">
              {recommendations.map((rec, index) => (
                <li key={index} className="d-flex align-items-center mb-2">
                  <img
                    src={rec.poster}
                    alt={rec.title}
                    className="img-thumbnail me-3"
                    style={{ width: '50px', height: '75px' }}
                  />
                  <span>{rec.title}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

export default MovieRecommendation;
