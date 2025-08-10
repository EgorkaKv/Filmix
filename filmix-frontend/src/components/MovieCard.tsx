import React from 'react';
import type { Movie } from '../types/Movie';
import './MovieCard.css';

interface MovieCardProps {
  movie: Movie;
}

const MovieCard: React.FC<MovieCardProps> = ({ movie }) => {
  return (
    <div className="movie-card">
      <div className="card-top">
        <div className="movie-poster">
          <img src={movie.poster_url} alt={movie.title} />
        </div>
        <div className="movie-info">
          {movie.original_title !== movie.title && (
            <p className="original-title">{movie.original_title}</p>
          )}
          <div className="movie-meta">
            <span className="year">{movie.year}</span>
            {/*<span className="director">Режиссёр: {movie.director}</span>*/}
            <div className="genres">
              {movie.genres.slice(0, 3).map((genre, index) => (
                <span key={index} className="genre">{genre}</span>
              ))}
            </div>
          </div>
          <div className="ratings">
            <span className="rating">⭐ {movie.rating.toFixed(1)}</span>
            {movie.my_rating && (
              <span className="my-rating">{movie.my_rating}</span>
            )}
          </div>
          {movie.watch_date && (
            <p className="watch-date">Просмотрено: {new Date(movie.watch_date).toLocaleDateString('ru-RU')}</p>
          )}
        </div>
      </div>
      <div className="card-bottom">
        <h3 className="movie-title">{movie.title}</h3>
      </div>
    </div>
  );
};

export default MovieCard;
