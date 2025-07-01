import json
import os


def ensure_data_dir(output_dir):
    os.makedirs(output_dir, exist_ok=True)


def load_movie_ids(filename):
    with open(filename) as f:
        return [line.strip() for line in f if line.strip()]


def save_data(movie_id, movie_data, credits_data, output_dir):
    ensure_data_dir(output_dir)
    path = os.path.join(output_dir, f"{movie_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"movie": movie_data, "credits": credits_data}, f, indent=2)
