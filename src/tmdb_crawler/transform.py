import csv
import sqlite3


def transform_to_csv(db_path):
    conn = sqlite3.connect(db_path)
    movie_rows = []
    person_rows = {}
    acted_in_rows = []

    for row in conn.execute("SELECT id, title, release_date FROM movies"):
        movie_id, movie_title, movie_year = row[0], row[1], row[2]
        year = movie_year.split("-")[0] if movie_year else ""
        movie_rows.append([movie_id, movie_title, year])

    for row in conn.execute(
        "SELECT movie_id, person_id, person_name, character FROM cast"
    ):
        person_id, movie_id, person_name, character = row[1], row[0], row[2], row[3]
        person_rows[person_id] = person_name
        acted_in_rows.append([person_id, movie_id, character])

    # Write films.csv with requested header
    with open("films.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["tconst:ID(Film)", "title", "year"])
        writer.writerows(movie_rows)

    # Write actors.csv with requested header
    with open("actors.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["nconst:ID(Actor)", "name", "lowercase_name"])
        for pid, name in person_rows.items():
            writer.writerow([pid, name, name.lower()])

    # Write acted_in.csv with requested header
    with open("acted_in.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([":START_ID(Actor)", ":END_ID(Film)", "character"])
        writer.writerows(acted_in_rows)

    print("CSV files created successfully.")
