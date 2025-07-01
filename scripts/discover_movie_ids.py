#!/usr/bin/env python3

import os
import sys
import time
import requests
from datetime import datetime

API_KEY = os.getenv("TMDB_API_KEY")
if not API_KEY:
    print("Error: TMDB_API_KEY not set in environment.")
    sys.exit(1)

BASE_URL = "https://api.themoviedb.org/3/discover/movie"
MAX_PAGES = 500
OUTPUT_FILE = "movie_ids.txt"
NEW_IDS_FILE = "new_movie_ids.txt"


def generate_yearly_date_ranges(start_year=1900):
    today = datetime.utcnow().date()
    current_year = today.year
    ranges = []
    for year in range(start_year, current_year):
        start = datetime(year, 1, 1).date()
        end = datetime(year, 12, 31).date()
        ranges.append((str(start), str(end)))
    # Add current year up to today
    start = datetime(current_year, 1, 1).date()
    end = today
    ranges.append((str(start), str(end)))
    return ranges


DATE_RANGES = generate_yearly_date_ranges()


def fetch_ids_for_range(start_date, end_date):
    ids = set()
    for page in range(1, MAX_PAGES + 1):
        params = {
            "api_key": API_KEY,
            "sort_by": "popularity.desc",
            "primary_release_date.gte": start_date,
            "primary_release_date.lte": end_date,
            "page": page,
            "vote_count.gte": 5,  # Only movies with at least 5 votes
            "include_adult": "false",  # Skip adult movies
        }
        response = requests.get(BASE_URL, params=params)
        if response.status_code != 200:
            print(f"Error {response.status_code}: {response.text}")
            break

        data = response.json()
        for movie in data.get("results", []):
            ids.add(str(movie["id"]))

        if page >= data.get("total_pages", 1):
            break

        time.sleep(0.15)  # Be polite

    print(f"Fetched {len(ids)} IDs for {start_date} to {end_date}")
    return ids


def main():
    # Load existing IDs
    existing_ids = set()
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r") as f:
            for line in f:
                existing_ids.add(line.strip())
        print(f"Loaded {len(existing_ids)} existing IDs.")

    # Collect new IDs
    new_ids = set()
    for start_date, end_date in DATE_RANGES:
        ids = fetch_ids_for_range(start_date, end_date)
        new_ids.update(ids)

    print(f"Fetched {len(new_ids)} IDs from this run.")

    # Merge
    all_ids = existing_ids.union(new_ids)
    print(f"Total unique IDs after merge: {len(all_ids)}")

    # Compute truly new IDs
    truly_new_ids = new_ids - existing_ids
    print(f"New IDs discovered this run: {len(truly_new_ids)}")

    # Save full list
    with open(OUTPUT_FILE, "w") as f:
        for mid in sorted(all_ids):
            f.write(mid + "\n")
    print(f"Updated {OUTPUT_FILE}.")

    # Save new IDs separately
    if truly_new_ids:
        with open(NEW_IDS_FILE, "w") as f:
            for mid in sorted(truly_new_ids):
                f.write(mid + "\n")
        print(f"Saved new IDs to {NEW_IDS_FILE}.")
    else:
        print("No new IDs were found. Skipping new_ids.txt creation.")


if __name__ == "__main__":
    main()
