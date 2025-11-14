thonpython
import json
import logging
import sys
from pathlib import Path

from extractors.review_parser import ReviewParser
from outputs.exporters import JSONExporter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

def load_app_urls(input_file: str):
    path = Path(input_file)
    if not path.exists():
        logging.error(f"Input file not found: {input_file}")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def main():
    if len(sys.argv) < 2:
        logging.error("Usage: python runner.py <input_urls.txt>")
        sys.exit(1)

    input_file = sys.argv[1]
    urls = load_app_urls(input_file)

    parser = ReviewParser()
    exporter = JSONExporter()

    all_results = []

    for url in urls:
        logging.info(f"Scraping reviews for: {url}")
        reviews = parser.fetch_reviews(url)
        all_results.extend(reviews)

    output_path = "reviews_output.json"
    exporter.export(all_results, output_path)

    logging.info(f"Scraping completed. Saved to {output_path}")

if __name__ == "__main__":
    main()