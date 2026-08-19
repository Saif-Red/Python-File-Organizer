import json
from pathlib import Path

HISTORY_FILE = Path("history.json")

def save_history(moves):
    """Save the latest organization operation."""

    data ={
        "moves": moves
    }

    with HISTORY_FILE.open(
        "w",
        encoding = "utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent = 4
        )

def load_history():
    """Load the latest organization operation."""

    if not HISTORY_FILE.exists():
        return []

    try:

        with HISTORY_FILE.open(
            "r",
            encoding = "utf-8"
        ) as file:

            data = json.load(file)

        return data.get(
            "moves",
            []
        )

    except (
        json.JSONDecodeError,
        OSError
    ):
        return []

def has_history():
    """Return True if an undoable organization exists."""

    return len(load_history()) > 0

def clear_history():
    """Remove the stored organization history."""

    if HISTORY_FILE.exists():
        HISTORY_FILE.unlink()