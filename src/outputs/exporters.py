thonpython
import json
import logging

class JSONExporter:
    def export(self, data, filepath: str):
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            logging.info(f"Exported {len(data)} records to {filepath}")
        except Exception as e:
            logging.error(f"Failed to export JSON: {e}")