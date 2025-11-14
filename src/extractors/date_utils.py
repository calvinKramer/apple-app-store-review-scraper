thonpython
from datetime import datetime

def parse_review_date(date_string: str) -> str:
    """Convert Apple date format to YYYY-MM-DD."""
    try:
        return datetime.fromisoformat(date_string.replace("Z", "")).strftime("%Y-%m-%d")
    except Exception:
        return date_string