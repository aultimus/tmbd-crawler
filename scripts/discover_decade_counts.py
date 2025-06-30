#!/usr/bin/env python3

import os
import sys
import requests
from datetime import datetime

API_KEY = os.getenv("TMDB_API_KEY")
if not API_KEY:
    print("Error: TMDB_API_KEY not set in environment.")
    sys.exit(1)

BASE_URL = "https://api.themoviedb.org/3/discover/movie"

# Define decades
DATE_RANGES = [
    ("1900-01-01", "1909-12-31"),
    ("1910-01-01", "1919-12-31"),
    ("1920-01-01", "1929-12-31"),
    ("1930-01-01", "1939-12-31"),
    ("1940-01-01", "1949-12-31"),
    ("1950-01-01", "1959-12-31"),
    ("1960-01-01", "1969-12-31"),
    ("1970-01-01", "1979-12-31"),
    ("1980-01-01", "1989-12-31"),
    ("1990-01-01", "1999-12-31"),
    ("2000-01-01", "2009-12-31"),
    ("2010-01-01", "2019-12-31"),
    ("2020-01-01", datetime.utcnow().strftime("%Y-%m-%d")),
]


def get_total_results(start_date, end_date):
    params = {
        "api_key": API_KEY,
        "primary_release_date.gte": start_date,
        "primary_release_date.lte": end_date,
        "sort_by": "popularity.desc",
        "page": 1,  # Just need the first page to see total_results
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
        return None
    data = response.json()
    return data.get("total_results", 0)


def main():
    print("Fetching total movie counts per decade...\n")
    for start_date, end_date in DATE_RANGES:
        total = get_total_results(start_date, end_date)
        if total is not None:
            print(f"{start_date} to {end_date}: {total} movies")
        else:
            print(f"{start_date} to {end_date}: ERROR fetching count")


if __name__ == "__main__":
    main()
