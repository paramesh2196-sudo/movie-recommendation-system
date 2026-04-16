"""
Movie Recommendation Engine
============================
Implements two recommendation strategies:
  1. Content-Based Filtering  — matches on genres, director, year
  2. Collaborative Filtering  — finds users with similar tastes (simulated)
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from data.movies import MOVIES


def _build_feature_string(movie: dict) -> str:
    """Creates a combined text feature for TF-IDF vectorization."""
    genres = " ".join(movie["genres"])
    director = movie["director"].replace(" ", "_")
    cast = " ".join(c.replace(" ", "_") for c in movie["cast"][:2])
    decade = str((movie["year"] // 10) * 10)
    return f"{genres} {genres} {director} {cast} {decade}"


class ContentBasedRecommender:
    """
    Recommends movies similar to a given movie using TF-IDF + cosine similarity
    on genre, director, cast, and decade features.
    """

    def __init__(self, movies: list = None):
        self.movies = movies or MOVIES
        self._build_matrix()

    def _build_matrix(self):
        features = [_build_feature_string(m) for m in self.movies]
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(features)
        self.similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
        self.id_to_idx = {m["id"]: i for i, m in enumerate(self.movies)}

    def recommend(self, movie_id: int, top_n: int = 5) -> list:
        """Returns top_n movies similar to the given movie_id."""
        if movie_id not in self.id_to_idx:
            return []
        idx = self.id_to_idx[movie_id]
        scores = list(enumerate(self.similarity_matrix[idx]))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)
        results = []
        for i, score in scores[1:]:          # skip the movie itself
            if len(results) >= top_n:
                break
            movie = dict(self.movies[i])
            movie["similarity_score"] = round(float(score), 3)
            results.append(movie)
        return results


class FilterEngine:
    """
    Filters movies based on user-selected criteria:
      - genres (list)
      - min_rating (float)
      - year_range (tuple)
      - platform (str)
    """

    def __init__(self, movies: list = None):
        self.movies = movies or MOVIES

    def filter(
        self,
        genres: list = None,
        min_rating: float = 0.0,
        year_from: int = 1900,
        year_to: int = 2100,
        platform: str = "All",
        sort_by: str = "rating",
    ) -> list:
        results = []
        for m in self.movies:
            if genres and not any(g in m["genres"] for g in genres):
                continue
            if m["rating"] < min_rating:
                continue
            if not (year_from <= m["year"] <= year_to):
                continue
            if platform != "All" and m["platform"] != platform:
                continue
            results.append(m)

        sort_key = {
            "rating": lambda x: x["rating"],
            "year": lambda x: x["year"],
            "title": lambda x: x["title"],
        }.get(sort_by, lambda x: x["rating"])

        return sorted(results, key=sort_key, reverse=(sort_by != "title"))


class HybridRecommender:
    """
    Combines content-based filtering with popularity/rating signals.
    Simulates collaborative filtering by using user preference vectors.
    """

    def __init__(self):
        self.content_rec = ContentBasedRecommender()
        self.filter_engine = FilterEngine()

    def recommend_by_preferences(
        self,
        liked_genres: list,
        min_rating: float = 7.0,
        platform: str = "All",
        top_n: int = 8,
    ) -> list:
        """Recommend movies based on user genre preferences."""
        filtered = self.filter_engine.filter(
            genres=liked_genres,
            min_rating=min_rating,
            platform=platform,
            sort_by="rating",
        )

        # Score = rating * genre_overlap_ratio
        for m in filtered:
            overlap = len(set(m["genres"]) & set(liked_genres))
            m["match_score"] = round(m["rating"] * (overlap / len(m["genres"])), 2)

        return sorted(filtered, key=lambda x: x["match_score"], reverse=True)[:top_n]
