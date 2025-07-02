import csv
import sqlite3


def transform_to_csv(db_path):
    conn = sqlite3.connect(db_path)
    movie_rows = []
    person_rows = {}
    acted_in_rows = []

    for row in conn.execute("SELECT id, title, release_date FROM movies"):
        movie_id, movie_title, _ = row[0], row[1], row[2]
        movie_rows.append([movie_id, movie_title])

    for row in conn.execute(
        "SELECT movie_id, person_id, person_name, character FROM cast"
    ):
        person_id, movie_id, person_name, character = row[1], row[0], row[2], row[3]
        person_rows[person_id] = person_name
        acted_in_rows.append([person_id, movie_id, character])

    # Write films.csv without year
    with open("films.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["tconst:ID(Film)", "title"])
        writer.writerows(movie_rows)

    # Write actors.csv with lowercase_name
    with open("actors.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["nconst:ID(Actor)", "name", "lowercase_name"])
        for pid, name in person_rows.items():
            writer.writerow([pid, name, name.lower()])

    # Write acted_in.csv
    with open("acted_in.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([":START_ID", ":END_ID", "character"])
        writer.writerows(acted_in_rows)

    print("CSV files created successfully.")
