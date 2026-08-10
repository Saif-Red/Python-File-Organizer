from pathlib import Path
import shutil
import logging

from config import FILE_CATEGORIES


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "organizer.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

def get_category(extension):
    extension = extension.lower()

    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category
    return "Others"

def get_unique_destination(destination):
    if not destination.exists():
        return destination

    counter = 1

    while True:
        new_name = f"{destination.stem}_{counter}{destination.suffix}"
        new_destination = destination.parent / new_name

        if not new_destination.exists():
            return new_destination

        counter += 1

def organize_folder(folder_path, dry_run=False):
    folder = Path(folder_path)

    if not folder.exists():
        return {
            "success": False,
            "dry_run": dry_run,
            "files_moved": 0,
            "files_failed": 0,
            "details": [],
            "error": "Folder does not exist."
        }

    if not folder.is_dir():
        return {
            "success": False,
            "dry_run": dry_run,
            "files_moved": 0,
            "files_failed": 0,
            "details": [],
            "error": "The selected path is not a folder."
        }

    logger.info(f"Started organization: {folder}")

    files_moved = 0
    files_failed = 0
    details = []

    for file in folder.iterdir():

        if not file.is_file():
            continue

        category = get_category(file.suffix)

        destination = folder / category
        target = destination / file.name

        target = get_unique_destination(target)

        if dry_run:
            message = f"[PREVIEW] {file.name} -> {target}"

            print(message)
            logger.info(
                f"Preview: {file.name} -> {target}"
            )

            details.append(message)

            files_moved += 1
            continue

        destination.mkdir(exist_ok=True)

        try:
            shutil.move(str(file), str(target))

            files_moved += 1

            message = f"Moved: {file.name} -> {target}"

            print(message)
            logger.info(message)

            details.append(message)

        except OSError as error:

            files_failed += 1

            message = (
                f"Could not move {file.name}: {error}"
            )

            print(message)
            logger.error(message)

            details.append(message)

    logger.info(
        f"Organization completed. "
        f"Moved: {files_moved}, "
        f"Failed: {files_failed}"
    )

    return {
        "success": True,
        "dry_run": dry_run,
        "files_moved": files_moved,
        "files_failed": files_failed,
        "details": details
    }