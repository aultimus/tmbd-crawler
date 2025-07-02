.PHONY: install develop crawl transform clean discover-movie-ids


pin-dependencies:
	pip install pip-tools
	pip-compile

# Install in editable mode
install-dependencies:
	pip install -r dev-requirements.txt
	pip install -e .

# Discover new movie IDs and update movie_ids.txt and new_movie_ids.txt
discover-movie-ids:
	python scripts/discover_movie_ids.py

# Run crawler
crawl:
	python scripts/crawl.py $(ARGS)

# Transform data to CSVs
transform:
	python scripts/transform.py

# Clean generated data and CSVs
clean:
	rm -f films.csv actors.csv acted_in.csv
