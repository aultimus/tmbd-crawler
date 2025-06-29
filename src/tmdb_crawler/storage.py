import json
import os
from .config import DATA_DIR


def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def load_movie_ids(filename):
    with open(filename) as f:
        return [line.strip() for line in f if line.strip()]


def save_data(movie_id, movie_data, credits_data):
    ensure_data_dir()
    path = os.path.join(DATA_DIR, f"{movie_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"movie": movie_data, "credits": credits_data}, f, indent=2)
