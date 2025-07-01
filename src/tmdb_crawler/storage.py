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
    # Remove crew from credits_data if present
    credits_data = dict(credits_data) if credits_data else {}
    if "crew" in credits_data:
        del credits_data["crew"]
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"movie": movie_data, "credits": credits_data}, f, indent=2)
