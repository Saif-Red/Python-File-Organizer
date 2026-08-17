import unittest
import tempfile

from pathlib import Path

from organizer import (
    get_category,
    get_unique_destination
)

class TestGetCategory(unittest.TestCase):
    def test_image_category(self):
        self.assertEqual(
            get_category(".jpg"),
            "Images"
        )

    def test_uppercase_image_extension(self):
        self.assertEqual(
            get_category(".JPG"),
            "Images"
        )

    def test_mixed_case_image_extension(self):
        self.assertEqual(
            get_category(".JpG"),
            "Images"
        )

    def test_document_category(self):
        self.assertEqual(
            get_category(".pdf"),
            "Documents"
        )

    def test_unknown_category(self):
        self.assertEqual(
            get_category(".xyz"),
            "Others"
        )

class TestUniqueDestination(unittest.TestCase):
    def test_new_destination_when_file_does_not_exist(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)

            destination = folder / "photo.jpg"

            result = get_unique_destination(
                destination
            )

            self.assertEqual(
                result,
                destination
            )

    def test_duplicate_destination(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)

            destination = folder / "photo.jpg"

            destination.touch()

            result = get_unique_destination(
                destination
            )

            self.assertEqual(
                result,
                folder / "photo_1.jpg"
            )

    def test_multiple_duplicates(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)

            (folder / "photo.jpg").touch()
            (folder / "photo_1.jpg").touch()
            (folder / "photo_2.jpg").touch()

            destination = folder / "photo.jpg"

            result = get_unique_destination(
                destination
            )

            self.assertEqual(
                result,
                folder / "photo_3.jpg"
            )

if __name__ == "__main__":
    unittest.main()