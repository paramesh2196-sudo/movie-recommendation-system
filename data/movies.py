"""
Sample movie dataset with genres, ratings, and metadata.
In a production system this would be loaded from TMDB API or MovieLens CSV.
"""

MOVIES = [
    {"id": 1,  "title": "The Dark Knight",       "genres": ["Action", "Crime", "Drama"],          "year": 2008, "rating": 9.0, "director": "Christopher Nolan", "cast": ["Christian Bale", "Heath Ledger"],       "platform": "Netflix"},
    {"id": 2,  "title": "Inception",              "genres": ["Action", "Sci-Fi", "Thriller"],      "year": 2010, "rating": 8.8, "director": "Christopher Nolan", "cast": ["Leonardo DiCaprio", "Joseph Gordon"],   "platform": "Netflix"},
    {"id": 3,  "title": "Interstellar",           "genres": ["Adventure", "Drama", "Sci-Fi"],      "year": 2014, "rating": 8.6, "director": "Christopher Nolan", "cast": ["Matthew McConaughey", "Anne Hathaway"], "platform": "Amazon Prime"},
    {"id": 4,  "title": "The Avengers",           "genres": ["Action", "Adventure", "Sci-Fi"],     "year": 2012, "rating": 8.0, "director": "Joss Whedon",        "cast": ["Robert Downey Jr.", "Chris Evans"],     "platform": "Disney+"},
    {"id": 5,  "title": "Avengers: Endgame",      "genres": ["Action", "Adventure", "Drama"],      "year": 2019, "rating": 8.4, "director": "Russo Brothers",      "cast": ["Robert Downey Jr.", "Chris Evans"],     "platform": "Disney+"},
    {"id": 6,  "title": "Parasite",               "genres": ["Comedy", "Drama", "Thriller"],       "year": 2019, "rating": 8.6, "director": "Bong Joon-ho",       "cast": ["Song Kang-ho", "Lee Sun-kyun"],         "platform": "Amazon Prime"},
    {"id": 7,  "title": "Joker",                  "genres": ["Crime", "Drama", "Thriller"],        "year": 2019, "rating": 8.4, "director": "Todd Phillips",       "cast": ["Joaquin Phoenix"],                      "platform": "Netflix"},
    {"id": 8,  "title": "The Shawshank Redemption","genres": ["Drama"],                             "year": 1994, "rating": 9.3, "director": "Frank Darabont",      "cast": ["Tim Robbins", "Morgan Freeman"],         "platform": "Netflix"},
    {"id": 9,  "title": "Forrest Gump",           "genres": ["Drama", "Romance"],                  "year": 1994, "rating": 8.8, "director": "Robert Zemeckis",     "cast": ["Tom Hanks", "Robin Wright"],            "platform": "Amazon Prime"},
    {"id": 10, "title": "The Lion King",          "genres": ["Animation", "Adventure", "Drama"],   "year": 1994, "rating": 8.5, "director": "Roger Allers",        "cast": ["Matthew Broderick", "Jeremy Irons"],    "platform": "Disney+"},
    {"id": 11, "title": "Pulp Fiction",           "genres": ["Crime", "Drama"],                    "year": 1994, "rating": 8.9, "director": "Quentin Tarantino",   "cast": ["John Travolta", "Samuel L. Jackson"],   "platform": "Amazon Prime"},
    {"id": 12, "title": "The Matrix",             "genres": ["Action", "Sci-Fi"],                  "year": 1999, "rating": 8.7, "director": "Wachowskis",          "cast": ["Keanu Reeves", "Laurence Fishburne"],   "platform": "Netflix"},
    {"id": 13, "title": "Spirited Away",          "genres": ["Animation", "Adventure", "Family"],  "year": 2001, "rating": 8.6, "director": "Hayao Miyazaki",      "cast": ["Daveigh Chase", "Suzanne Pleshette"],   "platform": "Netflix"},
    {"id": 14, "title": "3 Idiots",               "genres": ["Comedy", "Drama", "Romance"],        "year": 2009, "rating": 8.4, "director": "Rajkumar Hirani",     "cast": ["Aamir Khan", "R. Madhavan"],            "platform": "Netflix"},
    {"id": 15, "title": "Dangal",                 "genres": ["Action", "Biography", "Drama"],      "year": 2016, "rating": 8.4, "director": "Nitesh Tiwari",       "cast": ["Aamir Khan", "Fatima Sana Shaikh"],     "platform": "Netflix"},
    {"id": 16, "title": "KGF: Chapter 2",         "genres": ["Action", "Crime", "Drama"],          "year": 2022, "rating": 8.2, "director": "Prashanth Neel",      "cast": ["Yash", "Sanjay Dutt"],                  "platform": "Amazon Prime"},
    {"id": 17, "title": "RRR",                    "genres": ["Action", "Drama"],                   "year": 2022, "rating": 7.8, "director": "S.S. Rajamouli",      "cast": ["Jr. NTR", "Ram Charan"],               "platform": "Netflix"},
    {"id": 18, "title": "Baahubali 2",            "genres": ["Action", "Adventure", "Drama"],      "year": 2017, "rating": 8.2, "director": "S.S. Rajamouli",      "cast": ["Prabhas", "Rana Daggubati"],            "platform": "Netflix"},
    {"id": 19, "title": "The Godfather",          "genres": ["Crime", "Drama"],                    "year": 1972, "rating": 9.2, "director": "Francis Ford Coppola","cast": ["Marlon Brando", "Al Pacino"],            "platform": "Amazon Prime"},
    {"id": 20, "title": "Schindler's List",       "genres": ["Biography", "Drama", "History"],     "year": 1993, "rating": 9.0, "director": "Steven Spielberg",    "cast": ["Liam Neeson", "Ralph Fiennes"],          "platform": "Amazon Prime"},
    {"id": 21, "title": "Fight Club",             "genres": ["Drama", "Thriller"],                 "year": 1999, "rating": 8.8, "director": "David Fincher",        "cast": ["Brad Pitt", "Edward Norton"],           "platform": "Amazon Prime"},
    {"id": 22, "title": "Goodfellas",             "genres": ["Biography", "Crime", "Drama"],       "year": 1990, "rating": 8.7, "director": "Martin Scorsese",     "cast": ["Robert De Niro", "Ray Liotta"],          "platform": "Netflix"},
    {"id": 23, "title": "Avatar",                 "genres": ["Action", "Adventure", "Sci-Fi"],     "year": 2009, "rating": 7.9, "director": "James Cameron",        "cast": ["Sam Worthington", "Zoe Saldana"],       "platform": "Disney+"},
    {"id": 24, "title": "Get Out",                "genres": ["Horror", "Mystery", "Thriller"],     "year": 2017, "rating": 7.7, "director": "Jordan Peele",         "cast": ["Daniel Kaluuya"],                       "platform": "Amazon Prime"},
    {"id": 25, "title": "A Quiet Place",          "genres": ["Drama", "Horror", "Sci-Fi"],         "year": 2018, "rating": 7.5, "director": "John Krasinski",       "cast": ["Emily Blunt", "John Krasinski"],        "platform": "Amazon Prime"},
    {"id": 26, "title": "Spider-Man: No Way Home","genres": ["Action", "Adventure", "Sci-Fi"],     "year": 2021, "rating": 8.3, "director": "Jon Watts",            "cast": ["Tom Holland", "Zendaya"],               "platform": "Netflix"},
    {"id": 27, "title": "Oppenheimer",            "genres": ["Biography", "Drama", "History"],     "year": 2023, "rating": 8.9, "director": "Christopher Nolan",   "cast": ["Cillian Murphy", "Emily Blunt"],         "platform": "Amazon Prime"},
    {"id": 28, "title": "Barbie",                 "genres": ["Adventure", "Comedy", "Fantasy"],    "year": 2023, "rating": 6.9, "director": "Greta Gerwig",         "cast": ["Margot Robbie", "Ryan Gosling"],         "platform": "Amazon Prime"},
    {"id": 29, "title": "Everything Everywhere", "genres": ["Action", "Adventure", "Comedy"],      "year": 2022, "rating": 7.8, "director": "Daniels",              "cast": ["Michelle Yeoh", "Ke Huy Quan"],          "platform": "Netflix"},
    {"id": 30, "title": "Dune",                   "genres": ["Adventure", "Drama", "Sci-Fi"],      "year": 2021, "rating": 8.0, "director": "Denis Villeneuve",     "cast": ["Timothée Chalamet", "Zendaya"],          "platform": "Netflix"},
]

ALL_GENRES = sorted(set(g for m in MOVIES for g in m["genres"]))
ALL_PLATFORMS = sorted(set(m["platform"] for m in MOVIES))
