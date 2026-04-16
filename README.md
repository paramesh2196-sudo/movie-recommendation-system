# Movie Recommendation System

A Python-based movie recommendation system with a Streamlit web interface. Uses **content-based filtering** and **hybrid recommendations** to suggest movies based on your preferences.

## Features

- **Browse & Filter** — filter movies by genre, platform, rating, and year
- **Similar Movies** — find movies similar to one you liked (content-based filtering using TF-IDF + cosine similarity)
- **Personalised Picks** — get curated recommendations based on your genre preferences (hybrid filtering)
- Dataset of 30 popular movies across Netflix, Amazon Prime, and Disney+
- Clean, interactive Streamlit web UI
- CLI demo mode for quick testing

## Screenshots

```
┌─────────────────────────────────────────────────┐
│  🎬 Movie Recommendation System                  │
│  ─────────────────────────────────────────────  │
│  Sidebar:  ○ Browse & Filter                    │
│            ○ Similar Movies                     │
│            ○ Personalised Picks                 │
│                                                 │
│  [Genre ▼]  [Platform ▼]  [Min Rating ──────]  │
│                                                 │
│  🎬 The Dark Knight (2008)    ⭐ 9.0            │
│  Director: Christopher Nolan                    │
│  Genres: `Action` `Crime` `Drama`               │
│  Platform: 📺 Netflix                           │
└─────────────────────────────────────────────────┘
```

## Quick Start

### Web App
```bash
pip install -r requirements.txt
streamlit run app.py
```
Opens in browser at `http://localhost:8501`

### CLI Demo
```bash
pip install -r requirements.txt
python cli.py
```

## Project Structure

```
movie_recommendation/
├── app.py              # Streamlit web application
├── cli.py              # Command-line demo
├── recommender.py      # Recommendation algorithms
├── data/
│   ├── __init__.py
│   └── movies.py       # Movie dataset (30 movies)
└── requirements.txt    # Dependencies
```

## Recommendation Algorithms

### 1. Content-Based Filtering
Uses **TF-IDF vectorization** on movie features (genres, director, cast, decade) and computes **cosine similarity** to find movies closest to a selected title.

```
Movie Features → TF-IDF Matrix → Cosine Similarity → Top-N Similar Movies
```

### 2. Hybrid Filtering
Combines genre overlap scoring with IMDb ratings to produce a match score:
```
Match Score = IMDb Rating × (Genre Overlap / Total Genres)
```

### 3. Filter Engine
Multi-criteria hard filtering on genre, platform, year range, and minimum rating with configurable sort order.

## Tech Stack

| Component | Technology |
|-----------|------------|
| Web UI | Streamlit |
| ML | scikit-learn (TF-IDF, cosine similarity) |
| Data | NumPy, Pandas |
| Language | Python 3.10+ |

## Dataset

30 handpicked popular movies across genres including Action, Drama, Sci-Fi, Crime, Animation, Biography, and Horror. Platforms covered: Netflix, Amazon Prime, Disney+.

To extend with a larger dataset, replace `data/movies.py` with TMDB API integration or the MovieLens dataset.
