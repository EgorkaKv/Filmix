import React, { useState, useEffect } from 'react';
import MovieCard from '../components/MovieCard';
import Footer from '../components/Footer';
import type { Movie } from '../types/Movie';

const HomePage: React.FC = () => {
  const [movies, setMovies] = useState<Movie[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadMovies = async () => {
      try {
        setLoading(true);
        const apiUrl = import.meta.env.VITE_API_BASE_URL;
        const endpoint = import.meta.env.VITE_MOVIES_ENDPOINT;
        const response = await fetch(`${apiUrl}${endpoint}`);
        console.log(response);

        if (!response.ok) {
          throw new Error('Ошибка загрузки данных');
        }

        const data = await response.json();
        setMovies(data);
        setLoading(false);
      } catch (fetchError) {
        console.error('Ошибка при загрузке фильмов:', fetchError);
        setError('Ошибка загрузки фильмов');
        setLoading(false);
      }
    };

    loadMovies();
  }, []);

  if (loading) {
    return (
      <div className="app">
        <h1>Filmix</h1>
        <div className="loading">Загрузка фильмов...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="app">
        <h1>Filmix</h1>
        <div className="error">{error}</div>
      </div>
    );
  }

  return (
    <>
    <div className="app">
      <header className="app-header">
        <h1>Filmix</h1>
        <p>Мои просмотренные фильмы</p>
      </header>

      <main className="movies-container">
        {movies.length === 0 ? (
          <div className="no-movies">Фильмы не найдены</div>
        ) : (
          movies.map((movie) => (
            <MovieCard key={movie._id} movie={movie} />
          ))
        )}
      </main>


    </div>
      <Footer />
    </>
  );
};

export default HomePage;
