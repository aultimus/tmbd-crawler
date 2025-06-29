.PHONY: install develop crawl transform clean


pin-dependencies:
	pip install pip-tools
	pip-compile

# Install in editable mode
install-dependencies:
	pip install -r dev-requirements.txt
	pip install -e .

# Run crawler
crawl:
	python scripts/crawl.py

# Transform data to CSVs
transform:
	python scripts/transform.py

# Clean generated data and CSVs
clean:
	rm -rf data/*.json
	rm -f movies.csv people.csv acted_in.csv