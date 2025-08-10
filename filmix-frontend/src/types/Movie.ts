export interface Movie {
  title: string;
  original_title: string;
  original_language: string;
  series_name: string | null;
  year: number;
  director: string;
  genres: string[];
  rating: number;
  my_rating: number | null;
  watch_date: string | null;
  description: string;
  poster_url: string;
  content_type: "MOVIE" | "SERIES";
  _id: string;
}

export interface SearchMovie {
  tmdb_id: number;
  title: string;
  original_title: string;
  release_date: string;
  poster_path: string;
  overview: string;
  vote_average: number;
  content_type: "MOVIE" | "SERIES";
}

export interface SearchResponse {
  total_results: number;
  total_pages: number;
  current_page: number;
  results: SearchMovie[];
}
