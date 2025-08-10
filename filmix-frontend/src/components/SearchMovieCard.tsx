import React from 'react';
import type {SearchMovie} from '../types/Movie';
import './SearchMovieCard.css';

interface SearchMovieCardProps {
  movie: SearchMovie;
  onAdd: (tmdbId: number) => void;
  isAdding: boolean;
}

const SearchMovieCard: React.FC<SearchMovieCardProps> = ({ movie, onAdd, isAdding }) => {
  const handleAdd = () => {
    onAdd(movie.tmdb_id);
  };

  const getReleaseYear = (releaseDate: string) => {
    return releaseDate ? new Date(releaseDate).getFullYear() : 'Неизвестно';
  };

  return (
    <div className="search-movie-card">
      <div className="search-movie-poster">
        <img
          src={movie.poster_path || '/placeholder-poster.jpg'}
          alt={movie.title}
          onError={(e) => {
            (e.target as HTMLImageElement).src = '/placeholder-poster.jpg';
          }}
        />
      </div>
      <div className="search-movie-info">
        <h3 className="search-movie-title">{movie.title}</h3>
        {movie.original_title !== movie.title && (
          <p className="search-movie-original-title">{movie.original_title}</p>
        )}
        <p className="search-movie-year">Год: {getReleaseYear(movie.release_date)}</p>
        <p className="search-movie-rating">Рейтинг: {movie.vote_average.toFixed(1)}/10</p>
        <p className="search-movie-type">Тип: {movie.content_type === 'MOVIE' ? 'Фильм' : 'Сериал'}</p>
        <p className="search-movie-overview">{movie.overview || 'Описание недоступно'}</p>
        <button
          className="add-movie-button"
          onClick={handleAdd}
          disabled={isAdding}
        >
          {isAdding ? 'Добавляется...' : 'Добавить фильм'}
        </button>
      </div>
    </div>
  );
};

export default SearchMovieCard;
