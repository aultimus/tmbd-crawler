# tmbd-crawler

This project provides a way to bootstrap a TMDB dataset. It provides a flexible pipeline to **fetch movie and credit data from TMDb** (The Movie Database) and **transform it into Neo4j-compatible CSVs**.

It exists because TMDb offers a rich, structured dataset that is ideal for building graph representations of actors, movies, and relationships. The crawler makes it easy to collect, store, and transform this data reproducibly.

Here we:
* Discover available movie ids and filter out all adult films and minor productions `make discover-movies`
* Download metadata for the given IDs `make crawl`
* Transform the data into a neo4j importable form `make transform`

The final transform step converts the data into a form importable into a neo4j database optimised for the six degrees of separation problem.

## Installation

Create a virtual environment and install dependencies:

```
python3 -m venv .venv
source .venv/bin/activate
```

`make install` - Install dependencies into .venv

You must obtain a TMDb API key by signing up at TMDb.

All configuration is managed via environment variables.

Create a .env file in the project root:

```
TMDB_API_KEY=your_tmdb_api_key_here
```

## Running

The main workflow is managed via the Makefile. The output of each preceding step feeds into the following step:

- `make discover-movie-ids`
  Input: N/A
  Output: `movie_ids.txt, new_movie_ids.txt`
  Download all TMDb movie IDs to `movie_ids.txt` and new IDs since last run to `new_movie_ids.txt`. The new IDs file can be used for incremental fetches in the next crawl step.

- `make crawl`
  Input: `movie_ids.txt`
  Output: `sqlite.db`
  Run the crawler to download movie and credit JSON files for the given IDs. You can pass arguments to control concurrency and the input file:

  ```sh
  make crawl ARGS="--concurrent-requests 20 --movie-ids-file custom_ids.txt"
  ```
  - `--concurrent-requests` sets the number of concurrent requests (default: 10)
  - `--movie-ids-file` sets the path to the movie IDs file (default: movie_ids.txt)

- `make transform`
  Input: `sqlite.db`
  Output: `acted_in.csv, movies.csv, people.csv`
  Transform JSON data into CSV files ready for Neo4j import.

- `make clean`
  Remove all downloaded JSON and generated CSVs.


## Features

- Async crawler with configurable concurrency
- Incremental data collection
- Clean CSV export for bulk Neo4j import

## TODO
- Do a more comprehensive ID fetch that is not limited to 10k per decade
- Make filters configurable for library use
- Fetch familial relations
