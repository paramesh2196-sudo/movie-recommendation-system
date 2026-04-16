"""
Movie Recommendation System — Streamlit Web App
================================================
Run with:  streamlit run app.py
"""

import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from data.movies import MOVIES, ALL_GENRES, ALL_PLATFORMS
from recommender import ContentBasedRecommender, FilterEngine, HybridRecommender

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Cached resources ──────────────────────────────────────────────────────────
@st.cache_resource
def load_engines():
    return ContentBasedRecommender(), FilterEngine(), HybridRecommender()


content_rec, filter_engine, hybrid_rec = load_engines()


# ── Helper ────────────────────────────────────────────────────────────────────
def render_movie_card(movie: dict, show_score: bool = False, score_label: str = "Score"):
    genre_tags = " ".join(f"`{g}`" for g in movie["genres"])
    score_line = ""
    if show_score:
        key = "match_score" if "match_score" in movie else "similarity_score"
        val = movie.get(key, movie["rating"])
        score_line = f"**{score_label}:** {val}"

    with st.container():
        st.markdown(f"### 🎬 {movie['title']} ({movie['year']})")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**Director:** {movie['director']}")
            st.markdown(f"**Cast:** {', '.join(movie['cast'])}")
            st.markdown(f"**Genres:** {genre_tags}")
            st.markdown(f"**Platform:** 📺 {movie['platform']}")
        with col2:
            st.metric("IMDb Rating", f"⭐ {movie['rating']}")
            if score_line:
                st.markdown(score_line)
        st.divider()


# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.title("🎬 Movie Recommender")
st.sidebar.markdown("*Find your next favourite movie*")
mode = st.sidebar.radio(
    "Choose Mode",
    ["🔍 Browse & Filter", "🤝 Similar Movies", "⭐ Personalised Picks"],
)

# ── Main area ─────────────────────────────────────────────────────────────────
st.title("🎬 Movie Recommendation System")
st.markdown("Powered by **Content-Based Filtering** + **Hybrid Recommendations**")
st.divider()

# ────────────────────────────────────────────────────────────────────────────
# MODE 1: Browse & Filter
# ────────────────────────────────────────────────────────────────────────────
if mode == "🔍 Browse & Filter":
    st.header("Browse & Filter Movies")

    col1, col2, col3 = st.columns(3)
    with col1:
        selected_genres = st.multiselect("Genres", ALL_GENRES)
        platform = st.selectbox("Platform", ["All"] + ALL_PLATFORMS)
    with col2:
        min_rating = st.slider("Minimum Rating", 0.0, 10.0, 7.0, 0.1)
        sort_by = st.selectbox("Sort By", ["rating", "year", "title"])
    with col3:
        year_from = st.number_input("Year From", 1900, 2025, 1990)
        year_to = st.number_input("Year To", 1900, 2025, 2025)

    results = filter_engine.filter(
        genres=selected_genres if selected_genres else None,
        min_rating=min_rating,
        year_from=year_from,
        year_to=year_to,
        platform=platform,
        sort_by=sort_by,
    )

    st.markdown(f"**{len(results)} movies found**")
    st.divider()

    if results:
        for movie in results:
            render_movie_card(movie)
    else:
        st.info("No movies match your filters. Try adjusting the criteria.")

# ────────────────────────────────────────────────────────────────────────────
# MODE 2: Similar Movies (Content-Based)
# ────────────────────────────────────────────────────────────────────────────
elif mode == "🤝 Similar Movies":
    st.header("Find Movies Similar To...")
    st.markdown("Select a movie you liked and we'll find similar ones using **content-based filtering**.")

    movie_titles = [m["title"] for m in MOVIES]
    selected_title = st.selectbox("Select a Movie", movie_titles)
    top_n = st.slider("Number of Recommendations", 3, 10, 5)

    selected_movie = next(m for m in MOVIES if m["title"] == selected_title)

    st.subheader("Selected Movie")
    render_movie_card(selected_movie)

    st.subheader(f"Top {top_n} Similar Movies")
    recs = content_rec.recommend(selected_movie["id"], top_n=top_n)

    if recs:
        for movie in recs:
            render_movie_card(movie, show_score=True, score_label="Similarity")
    else:
        st.warning("Could not find similar movies.")

# ────────────────────────────────────────────────────────────────────────────
# MODE 3: Personalised Picks (Hybrid)
# ────────────────────────────────────────────────────────────────────────────
elif mode == "⭐ Personalised Picks":
    st.header("Personalised Movie Recommendations")
    st.markdown("Tell us your preferences and we'll curate the best picks for you.")

    col1, col2 = st.columns(2)
    with col1:
        fav_genres = st.multiselect(
            "Your Favourite Genres",
            ALL_GENRES,
            default=["Action", "Drama"],
        )
        platform = st.selectbox("Preferred Platform", ["All"] + ALL_PLATFORMS)
    with col2:
        min_rating = st.slider("Minimum Rating", 5.0, 10.0, 7.5, 0.1)
        top_n = st.slider("How many recommendations?", 3, 15, 8)

    if st.button("Get My Recommendations", type="primary"):
        if not fav_genres:
            st.warning("Please select at least one genre.")
        else:
            with st.spinner("Finding the best movies for you..."):
                recs = hybrid_rec.recommend_by_preferences(
                    liked_genres=fav_genres,
                    min_rating=min_rating,
                    platform=platform,
                    top_n=top_n,
                )

            if recs:
                st.success(f"Found {len(recs)} personalised recommendations!")
                for movie in recs:
                    render_movie_card(movie, show_score=True, score_label="Match Score")
            else:
                st.info("No movies matched your preferences. Try lowering the minimum rating.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.sidebar.divider()
st.sidebar.markdown("**Dataset:** 30 curated movies")
st.sidebar.markdown("**Algorithms:**")
st.sidebar.markdown("- TF-IDF + Cosine Similarity")
st.sidebar.markdown("- Genre-based Hybrid Filtering")
st.sidebar.markdown("---")
st.sidebar.markdown("Built for College Presentation 🎓")
