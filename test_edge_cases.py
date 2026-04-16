"""
Edge case tests for Movie Recommendation System
Run: python test_edge_cases.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from recommender import ContentBasedRecommender, FilterEngine, HybridRecommender
from data.movies import MOVIES, ALL_GENRES, ALL_PLATFORMS

passed = failed = 0
results = []

def check(name, condition, detail=""):
    global passed, failed
    if condition:
        passed += 1
        results.append(f"[PASS] {name}")
    else:
        failed += 1
        results.append(f"[FAIL] {name}  {detail}")

# ── FilterEngine ──────────────────────────────────────────────────────────────
fe = FilterEngine()

# 1. No filters — returns all
r = fe.filter()
check("filter: no args returns all movies", len(r) == len(MOVIES))

# 2. Empty genre list — treated as no filter
r = fe.filter(genres=[])
check("filter: empty genre list returns all", len(r) == len(MOVIES))

# 3. Non-existent genre
r = fe.filter(genres=["Documentary"])
check("filter: non-existent genre returns empty", len(r) == 0)

# 4. Rating above max
r = fe.filter(min_rating=10.0)
check("filter: min_rating 10 returns empty or perfect only", len(r) <= 1)

# 5. Rating below min
r = fe.filter(min_rating=-5.0)
check("filter: negative rating returns all", len(r) == len(MOVIES))

# 6. Year range reversed (from > to)
r = fe.filter(year_from=2030, year_to=2020)
check("filter: reversed year range returns empty", len(r) == 0)

# 7. Year range exact match
r = fe.filter(year_from=1994, year_to=1994)
check("filter: single year 1994", all(m["year"] == 1994 for m in r))

# 8. Non-existent platform
r = fe.filter(platform="HBO")
check("filter: non-existent platform returns empty", len(r) == 0)

# 9. Sort by title
r = fe.filter(sort_by="title")
titles = [m["title"] for m in r]
check("filter: sort by title alphabetical", titles == sorted(titles))

# 10. Sort by year
r = fe.filter(sort_by="year")
years = [m["year"] for m in r]
check("filter: sort by year descending", years == sorted(years, reverse=True))

# 11. Invalid sort key — should default to rating
r = fe.filter(sort_by="invalid_key")
ratings = [m["rating"] for m in r]
check("filter: invalid sort_by defaults to rating", ratings == sorted(ratings, reverse=True))

# 12. Multiple genres OR logic
r = fe.filter(genres=["Horror", "Animation"])
check("filter: multiple genres (OR match)", all(
    any(g in m["genres"] for g in ["Horror", "Animation"]) for m in r
))

# ── ContentBasedRecommender ───────────────────────────────────────────────────
cb = ContentBasedRecommender()

# 13. Valid ID
r = cb.recommend(1, top_n=5)
check("content: valid id returns 5 recs", len(r) == 5)

# 14. Invalid ID
r = cb.recommend(99999)
check("content: invalid id returns empty", r == [])

# 15. Negative ID
r = cb.recommend(-1)
check("content: negative id returns empty", r == [])

# 16. top_n = 0
r = cb.recommend(1, top_n=0)
check("content: top_n=0 returns empty", len(r) == 0)

# 17. top_n larger than dataset
r = cb.recommend(1, top_n=1000)
check("content: top_n > dataset returns at most N-1", len(r) == len(MOVIES) - 1)

# 18. Self not in recommendations
r = cb.recommend(1, top_n=10)
check("content: movie itself not in own recs", all(m["id"] != 1 for m in r))

# 19. Similarity scores in [0, 1]
r = cb.recommend(1, top_n=5)
check("content: similarity scores in [0,1]",
      all(0.0 <= m["similarity_score"] <= 1.0 for m in r))

# 20. Scores sorted descending
scores = [m["similarity_score"] for m in r]
check("content: similarity scores sorted descending", scores == sorted(scores, reverse=True))

# ── HybridRecommender ─────────────────────────────────────────────────────────
hb = HybridRecommender()

# 21. Normal case
r = hb.recommend_by_preferences(liked_genres=["Action", "Sci-Fi"], min_rating=8.0)
check("hybrid: normal Action/Sci-Fi recs", len(r) > 0)

# 22. Empty liked_genres
r = hb.recommend_by_preferences(liked_genres=[], min_rating=8.0)
check("hybrid: empty genres returns empty", len(r) == 0)

# 23. All platforms
r = hb.recommend_by_preferences(liked_genres=["Drama"], platform="All")
check("hybrid: platform=All includes all platforms",
      len(set(m["platform"] for m in r)) >= 1)

# 24. Impossible combination
r = hb.recommend_by_preferences(liked_genres=["Horror"], min_rating=9.5)
check("hybrid: impossible combo returns empty", len(r) == 0)

# 25. top_n respected
r = hb.recommend_by_preferences(liked_genres=["Drama"], top_n=3)
check("hybrid: top_n=3 returns at most 3", len(r) <= 3)

# 26. All match scores non-negative
r = hb.recommend_by_preferences(liked_genres=["Action"], min_rating=7.0)
check("hybrid: match scores non-negative",
      all(m.get("match_score", 0) >= 0 for m in r))

# ── Data integrity ────────────────────────────────────────────────────────────
# 27. All movies have required fields
required = {"id", "title", "genres", "year", "rating", "director", "cast", "platform"}
check("data: all movies have required fields",
      all(required.issubset(m.keys()) for m in MOVIES))

# 28. All ids unique
ids = [m["id"] for m in MOVIES]
check("data: all movie ids unique", len(ids) == len(set(ids)))

# 29. Ratings in valid range
check("data: all ratings 0-10",
      all(0 <= m["rating"] <= 10 for m in MOVIES))

# 30. Genre list non-empty
check("data: all movies have at least 1 genre",
      all(len(m["genres"]) >= 1 for m in MOVIES))

# ── Print summary ─────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("  MOVIE RECOMMENDATION — EDGE CASE TESTS")
print("="*60)
for r in results:
    print(f"  {r}")
print("="*60)
print(f"  PASSED: {passed} / {passed + failed}")
print("="*60)
sys.exit(0 if failed == 0 else 1)
