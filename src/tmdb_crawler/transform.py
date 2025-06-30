import os
import json
import csv


def transform_to_csv(data_dir):
    movie_rows = []
    person_rows = {}
    acted_in_rows = []

    for fname in os.listdir(data_dir):
        if not fname.endswith(".json"):
            continue
        path = os.path.join(data_dir, fname)
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        movie = data["movie"]
        credits = data["credits"]

        movie_id = movie["id"]
        movie_title = movie["title"]
        movie_year = movie.get("release_date", "").split("-")[0]

        movie_rows.append([movie_id, movie_title, movie_year])

        for cast in credits.get("cast", []):
            person_id = cast["id"]
            person_name = cast["name"]
            character = cast.get("character", "")

            person_rows[person_id] = person_name
            acted_in_rows.append([person_id, movie_id, character])

    # Write movies.csv
    with open("movies.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["movie_id:ID", "title", "year"])
        writer.writerows(movie_rows)

    # Write people.csv
    with open("people.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["person_id:ID", "name"])
        for pid, name in person_rows.items():
            writer.writerow([pid, name])

    # Write acted_in.csv
    with open("acted_in.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([":START_ID", ":END_ID", "character"])
        writer.writerows(acted_in_rows)

    print("CSV files created successfully.")
