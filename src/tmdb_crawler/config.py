import os

API_KEY = os.getenv("TMDB_API_KEY")
CONCURRENT_REQUESTS = int(os.getenv("CONCURRENT_REQUESTS", "10"))
DATA_DIR = os.getenv("DATA_DIR", "data")
MOVIE_IDS_FILE = os.getenv("MOVIE_IDS_FILE", "movie_ids.txt")
