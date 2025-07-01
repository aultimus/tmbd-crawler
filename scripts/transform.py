import argparse
from tmdb_crawler.transform import transform_to_csv

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transform TMDb SQLite data to CSV.")
    parser.add_argument(
        "--db-path",
        default="tmdb.db",
        help="Path to SQLite database (default: tmdb.db)",
    )
    args = parser.parse_args()
    transform_to_csv(args.db_path)
