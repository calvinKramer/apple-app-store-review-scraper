thonpython
import requests
import json
import re
import logging
from datetime import datetime

from .date_utils import parse_review_date

class AppStoreParser:
    """Parses app reviews using Apple's public RSS JSON feed."""

    def __init__(self):
        self.session = requests.Session()

    def extract_app_id(self, url: str) -> str:
        match = re.search(r"id(\d+)", url)
        if not match:
            raise ValueError(f"Invalid App Store URL: {url}")
        return match.group(1)

    def get_reviews(self, url: str):
        app_id = self.extract_app_id(url)
        rss_url = f"https://itunes.apple.com/us/rss/customerreviews/id={app_id}/sortBy=mostRecent/json"

        logging.debug(f"Fetching: {rss_url}")
        resp = self.session.get(rss_url, timeout=10)

        if resp.status_code != 200:
            raise RuntimeError(f"Failed to fetch reviews (status {resp.status_code})")

        data = resp.json()
        entries = data.get("feed", {}).get("entry", [])
        reviews = []

        # First entry is app metadata, skip it
        for item in entries[1:]:
            try:
                review = {
                    "reviewId": item["id"]["label"],
                    "username": item["author"]["name"]["label"],
                    "rating": int(item.get("im:rating", {}).get("label", 0)),
                    "reviewTitle": item["title"]["label"],
                    "reviewText": item["content"]["label"],
                    "reviewDate": parse_review_date(item["updated"]["label"]),
                    "appId": app_id,
                    "appUrl": url,
                }
                reviews.append(review)
            except Exception as e:
                logging.warning(f"Skipping review entry due to parse error: {e}")

        return reviews