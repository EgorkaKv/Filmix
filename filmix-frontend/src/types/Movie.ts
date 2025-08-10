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

