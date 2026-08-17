# Smart File Organizer

A Python desktop application that automatically organizes files into
category-based folders based on their file extensions.

The application provides a graphical interface built with Tkinter,
preview mode, duplicate filename handling, progress tracking,
logging, error handling, and automated tests.

## Features

- Automatically organizes files by extension
- Supports configurable file categories
- Preview changes before moving files
- Handles duplicate filenames safely
- Provides a graphical user interface
- Displays organization progress
- Provides detailed operation results
- Handles invalid folders and file movement errors
- Maintains an operation log
- Supports repeated organization runs safely
- Includes automated unit and integration tests


## File Categories

Files are organized according to the extension categories defined in
`config.py`.

Typical categories include:

- Images
- Documents
- Videos
- Music
- Archives
- Others

Unknown or unsupported file extensions are placed in the `Others`
category.

## Project Structure

```text
Smart-File-Organizer/
│
├── organizer.py          # Core file organization logic
├── gui.py                # Tkinter graphical interface
├── config.py             # File category configuration
├── README.md             # Project documentation
│
├── tests/
│   ├── __init__.py
│   └── test_organizer.py # Automated tests
│
└── logs/
    └── organizer.log    # Operation log

## Installation

### Requirements

- Python 3.10 or newer
- Windows
- Tkinter

### Clone the repository

```bash
git clone https://github.com/Saif-Red/Python-File-Organizer.git


# ▶️ Step 13.7 — Running the Application

Add:

```markdown
## Running the Application

Run the graphical application with:

```bash
python gui.py


# 🧪 Step 13.8 — Testing

Add:

```markdown
## Running Tests

The project includes automated tests for the file organization logic.

From the project root, run:

```bash
python -m unittest discover

## Technologies Used

- **Python** — Application logic
- **Tkinter** — Graphical user interface
- **pathlib** — File and directory path handling
- **shutil** — File movement
- **logging** — Application logging
- **unittest** — Automated testing
- **Git & GitHub** — Version control and project management

## Concepts Practiced

This project was developed to practice:

- Python functions
- Object-oriented programming concepts
- File handling
- Directory traversal
- Exception handling
- Path manipulation
- GUI programming
- Multithreading
- Callback functions
- Logging
- Configuration management
- Unit testing
- Integration testing
- Git and GitHub
- Software project structure

