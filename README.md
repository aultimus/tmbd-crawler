# tmbd-crawler

This project provides a flexible pipeline to **fetch movie and credit data from TMDb** (The Movie Database) and **transform it into Neo4j-compatible CSVs**.

It exists because TMDb offers a rich, structured dataset that is ideal for building graph representations of actors, movies, and relationships. The crawler makes it easy to collect, store, and transform this data reproducibly.

Here we:
* Download the latest TMDB movie id data dump
* Filter out all adult films and minor productions
* Work out which films need to be fetched against what we currently have downloaded
* Download the missing films and cast

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
CONCURRENT_REQUESTS=10
DATA_DIR=data
MOVIE_IDS_FILE=movie_ids.txt
```

## Running

`make crawl` - Run the crawler to download movie and credit JSON files
`make transform` - Transform JSON data into CSV files ready for Neo4j import
`make clean` - Remove all downloaded JSON and generated CSVs


## Features

- Async crawler with configurable concurrency
- Incremental data collection
- Clean CSV export for bulk Neo4j import
