import asyncio
import aiohttp
from tqdm import tqdm
from tmdb_crawler.fetcher import fetch_movie_and_credits
from tmdb_crawler.storage import load_movie_ids, save_data
from tmdb_crawler.config import API_KEY, CONCURRENT_REQUESTS, MOVIE_IDS_FILE


async def worker(movie_id, session, semaphore):
    async with semaphore:
        movie_data, credits_data = await fetch_movie_and_credits(
            session, API_KEY, movie_id
        )
        save_data(movie_id, movie_data, credits_data)


async def main():
    movie_ids = load_movie_ids(MOVIE_IDS_FILE)
    semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)

    async with aiohttp.ClientSession() as session:
        tasks = [worker(mid, session, semaphore) for mid in movie_ids]

        for f in tqdm(asyncio.as_completed(tasks), total=len(tasks)):
            await f


if __name__ == "__main__":
    asyncio.run(main())
