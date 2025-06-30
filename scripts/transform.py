import argparse
from tmdb_crawler.transform import transform_to_csv

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transform TMDb JSON data to CSV.")
    parser.add_argument(
        "--data-dir",
        default="data",
        help="Directory containing JSON files (default: data)",
    )
    args = parser.parse_args()
    transform_to_csv(args.data_dir)
