from pathlib import Path
import shutil
import logging

from config import FILE_CATEGORIES
from history import save_history, load_history, clear_history


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "organizer.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

def get_category(extension: str) -> str:
    """Return the category associated with a file extension."""
    extension = extension.lower()

    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category
    return "Others"

def get_unique_destination(destination: Path) -> Path:
    """Return a unique destination path when a filename already exists."""
    if not destination.exists():
        return destination

    counter = 1

    while True:
        new_name = f"{destination.stem}_{counter}{destination.suffix}"
        new_destination = destination.parent / new_name

        if not new_destination.exists():
            return new_destination

        counter += 1

def organize_folder(folder_path: str | Path, dry_run: bool = False, progress_callback = None):
    """
    Organize files in the selected folder into category folders.
    
    Files are categorized by extension. Existing filenames are
    preserved whenever possible, and duplicate names receive a
    numeric suffix.
    """
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
    moves = []

    files = [
        file for file in folder.iterdir()
        if file.is_file()
    ]

    if not files:
        logger.info(
            f"No files found in folder: {folder}"
        )

        return {
            "success": True,
            "dry_run": dry_run,
            "files_moved": 0,
            "files_failed": 0,
            "details": [],
            "message": "No files moved in the selected folder."
        }

    total_files = len(files)

    if progress_callback:
        progress_callback(0, total_files)

    for file in files:

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
            if progress_callback:
                progress_callback(
                    files_moved + files_failed,
                    total_files
                )
            continue

        destination.mkdir(exist_ok=True)

        try:
            shutil.move(str(file), str(target))

            files_moved += 1

            moves.append(
                {
                    "source": str(file),
                    "destination": str(target)
                }
            )

            message = f"Moved: {file.name} -> {target}"

            print(message)
            logger.info(message)

            details.append(message)

            if progress_callback:
                progress_callback(
                    files_moved + files_failed,
                    total_files
                )

        except OSError as error:

            files_failed += 1

            message = (
                f"Could not move {file.name}: {error}"
            )

            print(message)
            logger.error(message)

            details.append(message)

    if moves:
        save_history(moves)
    
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

def undo_last_organization(progress_callback = None):
    """
    Undo the most recent organization operation.
    
    Files are moved from their category folders back to
    their original locations.
    """

    moves = load_history()

    if not moves:
        return {
            "success": False,
            "files_restored": 0,
            "files_failed": 0,
            "details": [],
            "message": "There is no organization to undo."
        }

    files_restored = 0
    files_failed = 0
    details = []

    total_files = len(moves)

    if progress_callback:
        progress_callback(0, total_files)

    remaining_moves = []

    #Reverse order is important
    #The latest move is undone first
    for move in reversed(moves):
        source = Path(move["source"])
        destination = Path(move["destination"])

        #The destination is where the file currently exists.
        #The source is where it originally came from.

        if not destination.exists():

            message = (
                f"Could not undo: file not found:\n"
                f"{destination}"
            )

            details.append(message)
            files_failed += 1

            remaining_moves.append(move)

            if progress_callback:
                progress_callback(
                    files_restored + files_failed,
                    total_files
                )

            continue

        #Never overwrite an existing file.
        if source.exists():
            message = (
                f"Could not restore:\n"
                f"{source}\n\n"
                f"An existing file is already there."
            )

            details.append(message)
            files_failed += 1

            remaining_moves.append(move)

            if progress_callback:
                progress_callback(
                    files_restored + files_failed,
                    total_files
                )

            continue

        try:
            source.parent.mkdir(
                parents = True,
                exist_ok = True
            )    

            shutil.move(
                str(destination),
                str(source)
            )

            files_restored += 1

            message = (
                f"Restored: {destination.name} -> {source}"
            )

            print(message)
            logger.info(message)

            details.append(message)

        except OSError as error:
            files_failed += 1

            message = (
                f"Could not restore {destination.name}: "
                f"{error}"
            )

            print(message)
            logger.error(message)

            details.append(message)

            remaining_moves.append(move)

        if progress_callback:
            progress_callback(
                files_restored + files_failed,
                total_files
            )    

    #If everything was successfully restored,
    #there is nothing left to undo.
    if not remaining_moves:
        clear_history()

    else:
        #Keep only the operations that could not be undone.
        save_history(
            list(reversed(remaining_moves))
        )

    logger.info(
        f"Undo completed. "
        f"Restored: {files_restored}, "
        f"Failed: {files_failed}"
    )

    return {
        "success": True,
        "files_restored": files_restored,
        "files_failed": files_failed,
        "details": details
    }