import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import SearchMovieCard from '../components/SearchMovieCard';
import type {SearchResponse, SearchMovie} from '../types/Movie';
import './AddMoviePage.css';

const AddMoviePage: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<SearchMovie[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [addingMovieId, setAddingMovieId] = useState<number | null>(null);
  const [message, setMessage] = useState<{ text: string; type: 'success' | 'error' } | null>(null);

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      setMessage({ text: 'Введите название фильма для поиска', type: 'error' });
      return;
    }

    setIsSearching(true);
    setMessage(null);

    try {
      const apiUrl = import.meta.env.VITE_API_BASE_URL;
      const response = await fetch(`${apiUrl}/api/movies/search/tmdb?query=${encodeURIComponent(searchQuery)}`);

      if (!response.ok) {
        throw new Error('Ошибка поиска фильмов');
      }

      const data: SearchResponse = await response.json();
      setSearchResults(data.results);

      if (data.results.length === 0) {
        setMessage({ text: 'Фильмы не найдены', type: 'error' });
      }
    } catch (error) {
      console.error('Ошибка при поиске фильмов:', error);
      setMessage({ text: 'Ошибка при поиске фильмов', type: 'error' });
      setSearchResults([]);
    } finally {
      setIsSearching(false);
    }
  };

  const handleAddMovie = async (tmdbId: number) => {
    setAddingMovieId(tmdbId);
    setMessage(null);

    try {
      const apiUrl = import.meta.env.VITE_API_BASE_URL;
      const response = await fetch(`${apiUrl}/api/movies/add-from-tmdb/${tmdbId}`, {
        method: 'POST',
      });

      if (!response.ok) {
        throw new Error('Ошибка добавления фильма');
      }

      setMessage({ text: 'Фильм успешно добавлен!', type: 'success' });
      // Удаляем добавленный фильм из результатов поиска
      setSearchResults(prev => prev.filter(movie => movie.tmdb_id !== tmdbId));
    } catch (error) {
      console.error('Ошибка при добавлении фильма:', error);
      setMessage({ text: 'Ошибка при добавлении фильма', type: 'error' });
    } finally {
      setAddingMovieId(null);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <div className="add-movie-page">
      <header className="add-movie-header">
        <Link to="/" className="back-link">← Назад к списку фильмов</Link>
        <h1>Добавить фильм</h1>
      </header>

      <div className="search-section">
        <div className="search-input-container">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Введите название фильма..."
            className="search-input"
            disabled={isSearching}
          />
          <button
            onClick={handleSearch}
            disabled={isSearching || !searchQuery.trim()}
            className="search-button"
          >
            {isSearching ? 'Поиск...' : 'Найти'}
          </button>
        </div>

        {message && (
          <div className={`message ${message.type}`}>
            {message.text}
          </div>
        )}
      </div>

      <div className="search-results">
        {searchResults.map((movie) => (
          <SearchMovieCard
            key={movie.tmdb_id}
            movie={movie}
            onAdd={handleAddMovie}
            isAdding={addingMovieId === movie.tmdb_id}
          />
        ))}
      </div>
    </div>
  );
};

export default AddMoviePage;
