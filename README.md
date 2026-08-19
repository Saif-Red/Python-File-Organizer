# Smart File Organizer

A Python-based Windows desktop application that automatically organizes
files into category-based folders according to their file extensions.

The application provides a graphical interface built with Tkinter,
preview mode, duplicate filename protection, progress tracking,
operation history, undo functionality, logging, configuration support,
error handling, and automated tests.

---

## Features

- Automatically organizes files by extension
- Configurable file categories
- Preview changes before moving files
- Safely handles duplicate filenames
- Progress tracking during operations
- Detailed operation results
- Undo the most recent organization
- Prevents accidental overwriting during undo
- Operation history stored locally
- Activity logging
- Dark-themed graphical interface
- Windows title-bar theme support
- File, Edit, Tools, and Help menus
- "How to Use" and "About" dialogs
- Automated unit tests
- Standalone Windows executable

---

## How It Works

Files in the selected folder are categorized according to their
extensions.

For example:

```text
photo.jpg
report.pdf
song.mp3
archive.zip

may become:

Selected Folder/
│
├── Images/
│   └── photo.jpg
│
├── Documents/
│   └── report.pdf
│
├── Music/
│   └── song.mp3
│
└── Archives/
    └── archive.zip
```
Unknown or unsupported extensions are placed in the **Others** category.

---

## Duplicate File Handling

The application never intentionally overwrites an existing file.

If a destination filename already exists, a numeric suffix is added.

Examples:

```text
photo.jpg
photo_1.jpg
photo_2.jpg
photo_3.jpg
```

---

## Preview Mode

Before moving any files, users can select:

```text
Preview changes
```

Preview mode calculates the proposed organization without actually moving the files.

This allows the user to verify the operation before committing to it.

---

## Undo

The application records successful file movements in **history.json**.

The most recent organization can be reversed using:

```text
Edit → Undo Last Organization
```

or:

```text
Ctrl + z
```

Undo will not overwrite an existing file at the original location.

If the original location already contains a file, that particular operation is left in the history so it can be handled safely later.

---

## File Categories

Categories are configured through **config.json**.

Typical categories include:

- Images
- Documents
- Videos
- Music
- Archives
- Others

The configuration can be modified without changing the core organization logic.

---

## Logging

Application activity is recorded in:
```text
logs/organizer.log
```

The log contains information about organization operations, previews, successful movements, failures, and undo operations.

Runtime log files are intentionally excluded from Git.

---

## Project Structure

```text
Python-File-Organizer/
│
├── assets/
│   └── icon.ico
│
├── tests/
│   ├── __init__.py
│   ├── test_history.py
│   └── test_organizer.py
│
├── .gitignore
├── config.json
├── config.py
├── gui.py
├── history.py
├── main.py
├── organizer.py
├── README.md
├── requirements.txt
├── SmartFileOrganizer.spec
└── theme.py
```

---

### Important runtime/generated directories

The following directories/files are generated locally and are not included in the Git repository:
```text
.venv/
build/
dist/
logs/
history.json
__pycache__/
```

---

## Requirements

- Windows
- Python 3.10 or newer
- Tkinter
- PyInstaller for building the executable

The project uses only Python standard-library modules for its application logic.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Saif-Red/Python-File-Organizer.git
```

Enter the project directory:

```bash
cd Python-File-Organizer
```
Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```PowerShell
.venv\Scripts\Activate.ps1
```

Install the required packages:

```PowerShell
pip install -r requirements.txt
```

---

## Running the Application

Launch the graphical application:

```PowerShell
python gui.py
```

Alternatively, the original command-line interface can be launched with:

```PowerShell
python main.py
```

---

## Running Tests

The project includes automated tests for file organization, duplicate handling, preview mode, history management, and undo.

Run the complete test suite with:

```PowerShell
python -m unittest discover -v
```

Current test status:

```text
19 tests
OK
```

---

## Building the Windows Executable

The application can be packaged into a standalone Windows executable using PyInstaller.

Build command:

```PowerShell
python -m PyInstaller --onefile --windowed --add-data "config.json;." --name SmartFileOrganizer --icon assets/icon.ico --add-data "assets/icon.ico;assets" gui.py
```

The executable will be generated in:

```text
dist/
└── SmartFileOrganizer.exe
```

The **SmartFileOrganizer.spec** file is also included in the repository to preserve the PyInstaller build configuration.

---

## Technologies Used

- **Python**
- **Tkinter**
- **pathlib**
- **shutil**
- **json**
- **logging**
- **threading**
- **ctypes**
- **unittest**
- **PyInstaller**
- **Git**
- **GitHub**

---

## Concepts Practiced

This project was developed to practice and strengthen:
- Python programming
- Functions and modules
- File handling
- Directory traversal
- Exception handling
- Path manipulation
- JSON configuration
- GUI development
- Multithreading
- Callback functions
- Logging
- State/history management
- Undo functionality
- Unit testing
- Software project structure
- Virtual environments
- Git and GitHub
- Application packaging
- Windows executable creation

## Project Status

### Core Application Complete

The application has completed its main development phase, including:

- Core file organization
- GUI
- Preview mode
- Duplicate handling
- Progress tracking
- Logging
- Undo functionality
- Automated testing
- Windows executable packaging

The remaining work focuses on final documentation, screenshots, repository presentation, and release preparation.

## License

This project is intended as a personal learning and portfolio project.