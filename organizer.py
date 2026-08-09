from pathlib import Path
import shutil

from config import FILE_CATEGORIES

def get_category(extension):
    extension = extension.lower()

    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category
    return "Others"

def organize_folder(folder_path):
    folder = Path(folder_path)

    if not folder.exists():
        print("ERROR: Folder does not exist>")
        return

    if not folder.is_dir():
        print("ERROR: The selected path is not a folder.")
        return

    for file in folder.iterdir():
        if not file.is_file():
            continue

        category = get_category(file.suffix)
        destination = folder / category
        destination.mkdir(exist_ok = True)
        target = destination / file.name
        shutil.move(str(file), str(target))
        print(f"Moved: {file.name} -> {category}/")