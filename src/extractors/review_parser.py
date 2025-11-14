thonpython
import logging
import re
import requests
from .utils_date import normalize_date

class ReviewParser:
    APP_URL_REGEX = r"id(\d+)"
    RSS_URL_TEMPLATE = "https://itunes.apple.com/rss/customerreviews/id={}/json"

    def extract_app_id(self, app_url: str) -> str:
        match = re.search(self.APP_URL_REGEX, app_url)
        if not match:
            raise ValueError(f"Invalid Apple App Store URL: {app_url}")
        return match.group(1)

    def fetch_reviews(self, app_url: str):
        app_id = self.extract_app_id(app_url)
        rss_url = self.RSS_URL_TEMPLATE.format(app_id)

        try:
            resp = requests.get(rss_url, timeout=10)
            resp.raise_for_status()
        except Exception as e:
            logging.error(f"Request failed for {app_url}: {e}")
            return []

        data = resp.json()
        entries = data.get("feed", {}).get("entry", [])

        reviews = []
        # First entry is app metadata, skip if needed
        for entry in entries:
            if "im:rating" not in entry:
                continue

            reviews.append({
                "reviewerName": entry.get("author", {}).get("name", {}).get("label", ""),
                "rating": int(entry.get("im:rating", {}).get("label", 0)),
                "reviewTitle": entry.get("title", {}).get("label", ""),
                "reviewText": entry.get("content", {}).get("label", ""),
                "reviewDate": normalize_date(entry.get("updated", {}).get("label", "")),
                "appUrl": app_url
            })

        return reviews