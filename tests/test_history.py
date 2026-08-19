import unittest
import tempfile
from pathlib import Path
import history

from organizer import undo_last_organization

class TestHistory(unittest.TestCase):
    def setUp(self):
        self.original_history_file = history.HISTORY_FILE
        self.temp_dir = tempfile.TemporaryDirectory()
        history.HISTORY_FILE = (
            Path(self.temp_dir.name)
            / "history.json"
        )

    def tearDown(self):
        history.HISTORY_FILE = (
            self.original_history_file
        )
        self.temp_dir.cleanup()

    def test_save_and_load_history(self):
        moves = [
            {
                "source" : "photo.jpg",
                "destination": "Images/photo.jpg"
            }
        ]

        history.save_history(moves)

        result = history.load_history()

        self.assertEqual(
            result,
            moves
        )

    def test_empty_history(self):
        result = history.load_history()

        self.assertEqual(
            result,
            []
        )

    def test_clear_history(self):
        moves = [
            {
                "source": "photo.jpg",
                "destination": "Images/photo.jpg"
            }
        ]

        history.save_history(moves)
        history.clear_history()
        result = history.load_history()

        self.assertEqual(
            result,
            []
        )

if __name__ == "__main__":
    unittest.main()