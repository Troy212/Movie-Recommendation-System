import React, { useState, useEffect } from 'react';
// import 'bootstrap/dist/css/bootstrap.min.css';
import axios from 'axios';
import MovieRecommendation from './components/MovieRecommendation';


function App() {
  return (
    <div className='picture-background'>
      <h1></h1>
      <MovieRecommendation />
    </div>
  );
}

export default App;
