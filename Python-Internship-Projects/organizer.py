"""Task 3: Automated File Organizer & Cleanup Utility."""
import os
import shutil
from pathlib import Path

FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".ppt", ".pptx", ".xls", ".xlsx"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi"],
    "Music": [".mp3", ".wav", ".aac", ".flac"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp"],
}


def get_category(extension):
    """Return the category name for a file extension."""
    for category, extensions in FILE_CATEGORIES.items():
        if extension.lower() in extensions:
            return category
    return "Others"


def unique_destination(destination):
    """If a file with the same name exists, add _1, _2, ... to the name."""
    if not destination.exists():
        return destination
    counter = 1
    while True:
        candidate = destination.parent / f"{destination.stem}_{counter}{destination.suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def organize_folder(folder):
    """Move every file in the folder into a category subfolder."""
    moved = {}
    errors = []

    with os.scandir(folder) as entries:
        files = [Path(entry.path) for entry in entries if entry.is_file()]

    for file_path in files:
        category = get_category(file_path.suffix)
        target_folder = folder / category
        try:
            target_folder.mkdir(exist_ok=True)
            destination = unique_destination(target_folder / file_path.name)
            shutil.move(str(file_path), str(destination))
            moved[category] = moved.get(category, 0) + 1
            print(f"Moved: {file_path.name}  ->  {category}/{destination.name}")
        except PermissionError:
            errors.append(f"Permission denied: {file_path.name}")
        except FileExistsError:
            errors.append(f"File already exists: {file_path.name}")
        except OSError as error:
            errors.append(f"Could not move {file_path.name}: {error}")
    return moved, errors


def print_summary(moved, errors):
    print("\n" + "=" * 40)
    print("ORGANIZER SUMMARY")
    print("=" * 40)
    if moved:
        for category, count in sorted(moved.items()):
            print(f"{category:<12} : {count} file(s)")
        print(f"{'Total':<12} : {sum(moved.values())} file(s)")
    else:
        print("No files were moved.")
    if errors:
        print("\nProblems:")
        for message in errors:
            print(" -", message)
    print("=" * 40)


def main():
    default_folder = Path(__file__).parent / "Organizer-Test"
    print("FILE ORGANIZER")
    answer = input(f"Folder to organize (press Enter for {default_folder}): ").strip().strip('"')
    folder = Path(answer) if answer else default_folder

    if not folder.is_dir():
        print("That folder does not exist. Please check the path.")
        return

    confirm = input(f"Organize all files in '{folder}'? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Cancelled. No files were moved.")
        return

    moved, errors = organize_folder(folder)
    print_summary(moved, errors)


if __name__ == "__main__":
    main()
