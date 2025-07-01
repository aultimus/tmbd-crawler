import argparse
import asyncio
import aiohttp
import os
from datetime import datetime
from tqdm import tqdm
from tmdb_crawler.fetcher import fetch_movie_and_credits
from tmdb_crawler.storage import load_movie_ids, save_data_sqlite
from tmdb_crawler.config import API_KEY


def is_valid_movie(movie):
    # Check title is not empty
    if not movie.get("title"):
        return False, "Missing or empty title"
    # Check id exists
    if "id" not in movie:
        return False, "Missing id"
    # Check release_date is a valid date (YYYY-MM-DD)
    date_str = movie.get("release_date", "")
    if date_str:
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return False, f"Invalid release_date: {date_str}"
    # Filter out adult movies
    if movie.get("adult"):
        return False, "Adult movie filtered"
    return True, None


async def worker(movie_id, session, semaphore, db_path, incremental):
    # For incremental, check if movie already in DB
    import sqlite3

    if incremental and os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cur = conn.execute("SELECT 1 FROM movies WHERE id=?", (movie_id,))
        if cur.fetchone():
            conn.close()
            return
        conn.close()
    async with semaphore:
        movie_data, credits_data = await fetch_movie_and_credits(
            session, API_KEY, movie_id
        )
        if movie_data is None or credits_data is None:
            print(f"Skipping {movie_id} due to missing data (possibly 404)")
            return
        valid, reason = is_valid_movie(movie_data)
        if not valid:
            print(f"Skipping {movie_id}: {reason}")
            return
        save_data_sqlite(movie_id, movie_data, credits_data, db_path)


async def main(movie_ids_file, concurrent_requests, db_path, incremental):
    movie_ids = load_movie_ids(movie_ids_file)
    semaphore = asyncio.Semaphore(concurrent_requests)

    async with aiohttp.ClientSession() as session:
        tasks = [
            worker(mid, session, semaphore, db_path, incremental) for mid in movie_ids
        ]

        for f in tqdm(asyncio.as_completed(tasks), total=len(tasks)):
            await f


def parse_args():
    parser = argparse.ArgumentParser(description="Crawl TMDb movie and credit data.")
    parser.add_argument(
        "--movie-ids-file",
        default="movie_ids.txt",
        help="Path to file containing movie IDs (default: movie_ids.txt)",
    )
    parser.add_argument(
        "--concurrent-requests",
        type=int,
        default=10,
        help="Number of concurrent requests (default: 10)",
    )
    parser.add_argument(
        "--db-path",
        default="tmdb.db",
        help="Path to SQLite database (default: tmdb.db)",
    )
    parser.add_argument(
        "--incremental",
        action="store_true",
        help="Skip downloading if movie already exists in DB (default: False)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(
        main(
            args.movie_ids_file,
            args.concurrent_requests,
            args.db_path,
            args.incremental,
        )
    )
