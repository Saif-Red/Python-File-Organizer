import json
from pathlib import Path

CONFIG_FILE = Path(__file__).parent / "config.json"

def load_config():
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        print("ERROR: config.json was not found.")
        return {}

    except json.JSONDecodeError as error:
        print(f"ERROR: config.json contains invalid JSON")
        print(error)
        return {}

FILE_CATEGORIES = load_config()