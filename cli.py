"""
Movie Recommendation System — CLI Demo
=======================================
Run with: python cli.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from data.movies import MOVIES, ALL_GENRES, ALL_PLATFORMS
from recommender import ContentBasedRecommender, FilterEngine, HybridRecommender


def print_movie(movie: dict, idx: int = None, show_score: bool = False):
    prefix = f"{idx}. " if idx else "   "
    score = ""
    if show_score:
        key = "match_score" if "match_score" in movie else "similarity_score"
        score = f"  [Score: {movie.get(key, '—')}]"
    print(f"\n{prefix}{movie['title']} ({movie['year']})")
    print(f"   IMDb: ⭐ {movie['rating']}  |  Platform: {movie['platform']}{score}")
    print(f"   Genres: {', '.join(movie['genres'])}")
    print(f"   Director: {movie['director']}")


def demo_filter():
    print("\n" + "=" * 55)
    print("  DEMO 1: Filter — Action + Sci-Fi, Rating ≥ 8.0")
    print("=" * 55)
    engine = FilterEngine()
    results = engine.filter(genres=["Action", "Sci-Fi"], min_rating=8.0, sort_by="rating")
    for i, m in enumerate(results, 1):
        print_movie(m, i)


def demo_content_based():
    print("\n" + "=" * 55)
    print("  DEMO 2: Content-Based — Movies similar to 'Inception'")
    print("=" * 55)
    rec = ContentBasedRecommender()
    movie = next(m for m in MOVIES if m["title"] == "Inception")
    print_movie(movie)
    print("\n  Recommendations:")
    recs = rec.recommend(movie["id"], top_n=5)
    for i, m in enumerate(recs, 1):
        print_movie(m, i, show_score=True)


def demo_personalised():
    print("\n" + "=" * 55)
    print("  DEMO 3: Personalised — Drama + Crime fan, Rating ≥ 8.5")
    print("=" * 55)
    rec = HybridRecommender()
    recs = rec.recommend_by_preferences(
        liked_genres=["Drama", "Crime"],
        min_rating=8.5,
        platform="All",
        top_n=6,
    )
    for i, m in enumerate(recs, 1):
        print_movie(m, i, show_score=True)


def interactive():
    print("\n" + "=" * 55)
    print("  MOVIE RECOMMENDATION SYSTEM — Interactive Mode")
    print("=" * 55)
    print("\nAvailable Genres:")
    for i, g in enumerate(ALL_GENRES, 1):
        print(f"  {i:2}. {g}")

    genres_input = input("\nEnter genres you like (comma-separated, e.g. Action,Drama): ")
    genres = [g.strip() for g in genres_input.split(",") if g.strip()]

    rating_input = input("Minimum rating (e.g. 7.5): ")
    try:
        min_rating = float(rating_input)
    except ValueError:
        min_rating = 7.0

    print("\nPlatforms:", ", ".join(ALL_PLATFORMS))
    platform = input("Preferred platform (or All): ").strip() or "All"

    rec = HybridRecommender()
    recs = rec.recommend_by_preferences(liked_genres=genres, min_rating=min_rating, platform=platform)

    print(f"\n  Found {len(recs)} recommendations for you:\n")
    for i, m in enumerate(recs, 1):
        print_movie(m, i, show_score=True)

    print("\n  For the full web UI, run:  streamlit run app.py\n")


if __name__ == "__main__":
    print("\n🎬 MOVIE RECOMMENDATION SYSTEM")
    print("=" * 55)
    print("Running all demo modes...\n")

    demo_filter()
    demo_content_based()
    demo_personalised()

    print("\n" + "=" * 55)
    print("  All demos complete!")
    print("  Web app: streamlit run app.py")
    print("=" * 55 + "\n")
