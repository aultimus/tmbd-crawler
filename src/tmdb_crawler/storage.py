import json
import os
import sqlite3


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


def get_db_connection(db_path):
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def ensure_db_schema(conn):
    conn.execute(
        """CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        release_date TEXT,
        raw_json TEXT
    )"""
    )
    conn.execute(
        """CREATE TABLE IF NOT EXISTS cast (
        movie_id INTEGER,
        person_id INTEGER,
        person_name TEXT,
        character TEXT,
        PRIMARY KEY (movie_id, person_id, character),
        FOREIGN KEY (movie_id) REFERENCES movies(id)
    )"""
    )
    conn.commit()


def save_data_sqlite(movie_id, movie_data, credits_data, db_path):
    conn = get_db_connection(db_path)
    ensure_db_schema(conn)
    # Insert movie
    conn.execute(
        "REPLACE INTO movies (id, title, release_date, raw_json) VALUES (?, ?, ?, ?)",
        (
            movie_data["id"],
            movie_data["title"],
            movie_data.get("release_date", None),
            json.dumps(movie_data),
        ),
    )
    # Insert cast
    if credits_data and "cast" in credits_data:
        for cast in credits_data["cast"]:
            conn.execute(
                "REPLACE INTO cast (movie_id, person_id, person_name, character) VALUES (?, ?, ?, ?)",
                (
                    movie_id,
                    cast["id"],
                    cast["name"],
                    cast.get("character", ""),
                ),
            )
    conn.commit()
    conn.close()
