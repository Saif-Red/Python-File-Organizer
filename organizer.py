from pathlib import Path
import shutil

from config import FILE_CATEGORIES

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
        print("ERROR: Folder does not exist")
        return

    if not folder.is_dir():
        print("ERROR: The selected path is not a folder.")
        return

    files_moved = 0
    files_failed = 0
    for file in folder.iterdir():
        if not file.is_file():
            continue

        category = get_category(file.suffix)
        destination = folder / category
        target = destination / file.name
        target = get_unique_destination(target)

        if dry_run:
            print(f"[PREVIEW] {file.name} -> {target}")
            files_moved += 1
            continue
        
        destination.mkdir(exist_ok = True)

        try:
            shutil.move(str(file), str(target))
            files_moved += 1
            print(f"Moved: {file.name} -> {target}")
        except OSError as error:
            files_failed += 1
            print(f"Could not move {file.name}: {error}")

        if dry_run:
            print("\n================================")
            print("           PREVIEW")
            print("================================")
            print(f"Files that would be moved: {files_moved}")
            print("No files were moved.")
        else:
            print("\n================================")
            print("           SUMMARY")
            print("================================")
            print(f"Files moved:  {files_moved}")
            print(f"Files failed: {files_failed}")
            print("================================")