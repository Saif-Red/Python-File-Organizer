import unittest
import tempfile

from pathlib import Path

from organizer import (
    get_category,
    get_unique_destination,
    organize_folder
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

class TestOrganizeFolder(unittest.TestCase):
    def test_organize_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)

            image = folder / "photo.jpg"
            document = folder / "report.pdf"
            music = folder / "song.mp3"
            unknown = folder / "mystery.xyz"

            image.touch()
            document.touch()
            music.touch()
            unknown.touch()

            result = organize_folder(folder)

            self.assertTrue(
                (folder / "Images" / "photo.jpg").exists()
            )

            self.assertTrue(
                (folder / "Documents" / "report.pdf").exists()
            )

            self.assertTrue(
                (folder / "Music" / "song.mp3").exists()
            )

            self.assertTrue(
                (folder / "Others" / "mystery.xyz").exists()
            )

    def test_organize_duplicate_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)

            images_folder = folder / "Images"
            images_folder.mkdir()

            existing_file = images_folder / "photo.jpg"
            existing_file.touch()

            new_file = folder / "photo.jpg"
            new_file.touch()

            organize_folder(folder)

            self.assertTrue(
                (images_folder / "photo.jpg").exists()
            )

            self.assertTrue(
                (images_folder / "photo_1.jpg").exists()
            )

    def test_dry_run_does_not_move_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)

            image = folder / "photo.jpg"
            image.touch()

            organize_folder(
                folder,
                dry_run = True
            )

            self.assertTrue(
                image.exists()
            )

            self.assertFalse(
                (folder / "Images" / "photo.jpg").exists()
            )

    def test_empty_folder(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)
            result = organize_folder(folder)

            self.assertEqual(
                result["files_moved"],
                0
            )

            self.assertEqual(
                result["files_failed"],
                0
            )

    def test_existing_directories_are_ignored(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)

            images = folder / "Images"
            documents = folder / "Documents"

            images.mkdir()
            documents.mkdir()

            organize_folder(folder)

            self.assertTrue(
                images.exists()
            )

            self.assertTrue(
                documents.exists()
            )

if __name__ == "__main__":
    unittest.main()