# Movie Recommendation System

A Python-based movie recommendation system with a **Streamlit web interface**. Uses **content-based filtering** (TF-IDF + cosine similarity) and **hybrid filtering** to suggest movies based on your preferences.

---

## Table of Contents
1. [What It Does](#what-it-does)
2. [Architecture](#architecture)
3. [How the Algorithms Work](#how-the-algorithms-work)
4. [Project Structure](#project-structure)
5. [Setup on a New Laptop](#setup-on-a-new-laptop)
6. [Running the Project](#running-the-project)
7. [Testing](#testing)
8. [Troubleshooting](#troubleshooting)
9. [Tech Stack](#tech-stack)

---

## What It Does

Three recommendation modes in one app:

| Mode | What It Does | Algorithm |
|------|-------------|-----------|
| **Browse & Filter** | Filter by genre, platform, rating, year | Multi-criteria hard filter |
| **Similar Movies** | "If you liked X, try these..." | TF-IDF + cosine similarity |
| **Personalised Picks** | Custom picks based on your genre preferences | Hybrid (genre match × rating) |

Ships with a curated dataset of **30 popular movies** across Netflix, Amazon Prime, and Disney+.

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Streamlit Web UI (app.py)         │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐   │
│  │ Browse & │  │ Similar  │  │ Personalised     │   │
│  │ Filter   │  │ Movies   │  │ Picks            │   │
│  └─────┬────┘  └─────┬────┘  └─────────┬────────┘   │
└────────┼────────────┼─────────────────┼─────────────┘
         │            │                 │
         ▼            ▼                 ▼
    ┌─────────┐  ┌────────────┐  ┌──────────────┐
    │ Filter  │  │ Content-   │  │ Hybrid       │
    │ Engine  │  │ Based      │  │ Recommender  │
    │         │  │ (TF-IDF)   │  │              │
    └────┬────┘  └─────┬──────┘  └──────┬───────┘
         │             │                │
         └─────────────┴────────────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ data/movies.py  │  (30 movies)
              └─────────────────┘
```

All logic lives in `recommender.py`; the UI layer in `app.py` just calls into these engines.

---

## How the Algorithms Work

### 1. Filter Engine (`FilterEngine` class)
Pure hard-filter. Takes user criteria and returns matching rows:
```
For each movie:
    if genres don't match    → skip
    if rating < min_rating   → skip
    if year out of range     → skip
    if platform doesn't match→ skip
    include it

Then sort by (rating | year | title) descending
```
Multiple genres use **OR logic** — a movie passes if it has *any* of the selected genres.

### 2. Content-Based Recommender (`ContentBasedRecommender` class)
Finds movies similar to a given movie using **TF-IDF vectorization** + **cosine similarity**.

**Step-by-step:**
1. Build a text "feature" per movie by concatenating genres (weighted 2x), director, top cast, decade:
   ```
   "Action Action Sci-Fi Sci-Fi Christopher_Nolan Leonardo_DiCaprio 2010s"
   ```
2. Run **TF-IDF** over all 30 features → 30×N matrix (N = vocab size)
3. Compute **cosine similarity** pairwise → 30×30 similarity matrix
4. For recommendations: look up the movie's row, sort columns by score, skip the movie itself, return top N
5. Scores are normalized between **0.0 and 1.0**

**Why this works:** Movies with overlapping genres, directors, and era share similar token distributions, so cosine distance captures "feel" similarity.

### 3. Hybrid Recommender (`HybridRecommender` class)
Combines hard filtering with a custom score:
```
match_score = rating × (liked_genres ∩ movie.genres) / len(movie.genres)
```
**Example:** A Drama-Crime movie would score high for a "Drama + Crime" preference, while a Drama-Comedy-Romance movie would score lower (only 1/3 overlap).

Workflow:
1. Filter by genres + min rating + platform
2. Compute match score for each remaining movie
3. Return top N sorted by match score

---

## Project Structure

```
movie_recommendation/
├── app.py              # Streamlit web UI
├── cli.py              # CLI demo runner
├── recommender.py      # FilterEngine + ContentBased + Hybrid classes
├── test_edge_cases.py  # 30 automated tests
├── data/
│   ├── __init__.py
│   └── movies.py       # Movie dataset (30 movies, 8 fields each)
├── requirements.txt    # Python dependencies
├── .gitignore          # Excludes venv, __pycache__
└── README.md           # This file
```

---

## Setup on a New Laptop

### Prerequisites
- **Python 3.10+** — [download here](https://www.python.org/downloads/)
- **Git** — [download here](https://git-scm.com/downloads)
- A terminal (Command Prompt / PowerShell / Terminal)

### Step 1 — Clone the repository
```bash
git clone https://github.com/paramesh2196-sudo/movie-recommendation-system.git
cd movie-recommendation-system
```

### Step 2 — Create a virtual environment (recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```
This installs pandas, numpy, scikit-learn, Streamlit, and Pillow.

### Step 4 — Verify the install
```bash
python -X utf8 test_edge_cases.py
```
You should see **`PASSED: 30 / 30`** at the bottom.

---

## Running the Project

### Option A — Web UI (Recommended)
```bash
streamlit run app.py
```
Opens automatically in browser at **http://localhost:8501**.

**Three modes in the sidebar:**

1. **🔍 Browse & Filter**
   - Select genres, platform, rating, year range
   - Results update live as you tweak filters
   - Sort by rating, year, or title

2. **🤝 Similar Movies**
   - Pick any movie from the dropdown
   - Get the top N most similar movies with similarity scores
   - Great for "I liked X, what else?" questions

3. **⭐ Personalised Picks**
   - Select your favorite genres
   - Set minimum rating & preferred platform
   - Click the button → get custom-ranked recommendations with match scores

### Option B — CLI Demo
```bash
python -X utf8 cli.py
```
Runs all 3 demo modes in the terminal with sample inputs — no UI needed.

---

## Testing

```bash
python -X utf8 test_edge_cases.py
```
Expected: **30 / 30 PASSED**

Tests cover:
- **Filter engine (12 tests):** no args, empty genre, non-existent genre, rating bounds, reversed year range, invalid platform, all sort modes, OR-logic
- **Content-based (8 tests):** valid/invalid/negative IDs, `top_n=0`, oversized top_n, self-exclusion, score range, sort order
- **Hybrid (6 tests):** normal case, empty genres, all platforms, impossible combos, top_n respected, non-negative scores
- **Data integrity (4 tests):** required fields present, unique IDs, rating range, non-empty genres

---

## Troubleshooting

### UnicodeEncodeError on Windows
```bash
python -X utf8 cli.py
```
(Streamlit handles UTF-8 natively, so `streamlit run app.py` works without the flag.)

### Port 8501 already in use
```bash
streamlit run app.py --server.port 8502
```

### `ModuleNotFoundError: No module named 'sklearn'`
```bash
pip install -r requirements.txt
```

### Streamlit shows blank page
- Hard refresh the browser (Ctrl+Shift+R / Cmd+Shift+R)
- Check terminal for errors
- Try a different browser (Streamlit works best in Chrome)

### Can't clone because of credentials
```bash
git clone https://github.com/paramesh2196-sudo/movie-recommendation-system.git
```
If prompted for a password, use a **GitHub Personal Access Token** instead of your password (see [docs](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)).

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Web UI | **Streamlit** 1.35.0 |
| ML | **scikit-learn** 1.4.2 (TF-IDF, cosine similarity) |
| Data | **NumPy** 1.26.4, **Pandas** 2.2.2 |
| Language | **Python 3.10+** |
| Testing | Custom test runner (no external deps) |

---

## Extending the Project

### Use a larger dataset
Replace `data/movies.py` with:
- **MovieLens dataset** — https://grouplens.org/datasets/movielens/ (10M+ ratings)
- **TMDB API** — https://www.themoviedb.org/documentation/api (live movie data)

The `FilterEngine` and `ContentBasedRecommender` interfaces will keep working — you just need to return a list of dicts with the same keys (`id`, `title`, `genres`, `year`, `rating`, `director`, `cast`, `platform`).

### Add collaborative filtering
The current hybrid recommender simulates collaborative signal via genre overlap. To add real collaborative filtering:
1. Collect user ratings in a CSV
2. Build a user-item matrix
3. Use `sklearn.decomposition.TruncatedSVD` or `surprise` library for matrix factorization
4. Merge with content-based scores

---

## License

MIT — free for learning, college projects, or production use.
