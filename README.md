# Smart File Organizer
A Python-based file organization utility that automatically sorts files into categorized folders based on their extensions.

## Features

- Automatically organizes files by extension
- Supports configurable file categories
- Preview / dry-run mode
- Confirmation before moving files
- Duplicate filename protection
- Error handling
- Operation logging
- JSON-based configuration
- Summary of organized files
- Command-line interface

## Technologies Used

- Python
- JSON
- Git
- GitHub

### Python Modules

- pathlib
- shutil
- json
- logging

## Project Structure

```text
Python-File-Organizer/
│
├── config.json
├── config.py
├── main.py
├── organizer.py
├── requirements.txt
├── README.md
└── .gitignore

```
The `logs/` directory is generated automatically when the application runs and is excluded from Git.

## Installation

1. git clone <repository-url>
2. cd Python-File-Organizer
3. python -m venv .venv
4. .venv\Scripts\activate
5. pip install -r requirements.txt

## Running the Application

Run:

```bash
python main.py

```markdown
## Preview Mode

Preview mode allows you to see what the application intends to do without actually moving files.

Choose:

```text
1. Preview changes

Then:

```markdown
## Organize Files

Choose:

```text
2. Organize files


---

This is particularly important now.

Explain:

```markdown
## Configuration

File categories and extensions are stored in `config.json`.

For example:

```json
{
    "Images": [
        ".jpg",
        ".png"
    ],
    "Documents": [
        ".pdf",
        ".docx"
    ]
}


```markdown
## Logging

The application records operations in:

```text
logs/organizer.log


---

This is one of the most useful sections.

Before:

```text
Downloads/
├── photo.jpg
├── assignment.pdf
├── song.mp3
├── program.py
└── movie.mp4

After:

Downloads/
├── Images/
│   └── photo.jpg
│
├── Documents/
│   └── assignment.pdf
│
├── Music/
│   └── song.mp3
│
├── Code/
│   └── program.py
│
└── Videos/
    └── movie.mp4


## Current Limitations

- The current version uses a command-line interface.
- Files are organized based on their extensions.
- The application currently targets local filesystem organization.
- There is no automatic background monitoring yet.

## Future Improvements

- Graphical user interface
- Windows executable
- Automatic folder monitoring
- More advanced file classification
- Custom user-defined rules
- Improved configuration management

## Author

Mohd Saif Ansari
mohdsaif1808@gmail.com