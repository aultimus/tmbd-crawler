import aiohttp
import asyncio

BASE_URL = "https://api.themoviedb.org/3"


async def fetch_json(session, url, params):
    for attempt in range(5):
        async with session.get(url, params=params) as resp:
            if resp.status == 200:
                return await resp.json()
            elif resp.status == 404:
                print(f"Not found (404): {url}")
                return None
            elif resp.status == 429:
                retry_after = int(resp.headers.get("Retry-After", "1"))
                print(f"Rate limited. Sleeping for {retry_after} seconds.")
                await asyncio.sleep(retry_after)
            else:
                resp.raise_for_status()
    raise Exception(f"Failed to fetch {url}")


async def fetch_movie_and_credits(session, api_key, movie_id):
    params = {"api_key": api_key}
    movie_url = f"{BASE_URL}/movie/{movie_id}"
    credits_url = f"{BASE_URL}/movie/{movie_id}/credits"

    movie_task = asyncio.create_task(fetch_json(session, movie_url, params))
    credits_task = asyncio.create_task(fetch_json(session, credits_url, params))

    movie_data, credits_data = await asyncio.gather(movie_task, credits_task)
    return movie_data, credits_data
