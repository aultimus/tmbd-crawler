import argparse
import asyncio
import aiohttp
from tqdm import tqdm
from tmdb_crawler.fetcher import fetch_movie_and_credits
from tmdb_crawler.storage import load_movie_ids, save_data
from tmdb_crawler.config import API_KEY


async def worker(movie_id, session, semaphore, output_dir):
    async with semaphore:
        movie_data, credits_data = await fetch_movie_and_credits(
            session, API_KEY, movie_id
        )
        save_data(movie_id, movie_data, credits_data, output_dir=output_dir)


async def main(movie_ids_file, concurrent_requests, output_dir):
    movie_ids = load_movie_ids(movie_ids_file)
    semaphore = asyncio.Semaphore(concurrent_requests)

    async with aiohttp.ClientSession() as session:
        tasks = [worker(mid, session, semaphore, output_dir) for mid in movie_ids]

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
        "--output-dir",
        default="data",
        help="Directory to store output JSON files (default: data)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(main(args.movie_ids_file, args.concurrent_requests, args.output_dir))
