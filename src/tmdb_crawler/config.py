import os

API_KEY = os.getenv("TMDB_API_KEY")
CONCURRENT_REQUESTS = int(os.getenv("CONCURRENT_REQUESTS", "10"))
