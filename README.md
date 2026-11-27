# expense-tracker
# File-organizer

A small Python toolkit for tidying and moving files. It has two tools:

- **File Organizer** (`file_checker.py`): a command-line script that sorts the files in a folder into category subfolders such as Images, Videos and Documents.
- **Smart File Transfer** (`file_transfer_ui.py`): a PyQt6 desktop app that copies files to a destination folder with drag and drop, a progress bar, speed and ETA readouts, and pause/resume.

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![PyQt6](https://img.shields.io/badge/GUI-PyQt6-41cd52)
![License](https://img.shields.io/badge/license-MIT-green)

<!-- Add a screenshot of the transfer window here:
![Smart File Transfer](docs/transfer-ui.png)
-->

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Building an Executable](#building-an-executable)
- [Limitations](#limitations)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

## Features

### File Organizer (CLI)

- Sorts files in a folder into subfolders by extension
- Creates category folders only when needed
- Skips existing subfolders and moves unrecognized files to `Others`
- Prints each move as it happens

| Folder | Extensions |
| --- | --- |
| Images | `.jpg` `.jpeg` `.png` `.gif` `.bmp` `.webp` |
| Videos | `.mp4` `.mkv` `.avi` `.mov` |
| Music | `.mp3` `.wav` `.aac` |
| Documents | `.pdf` `.docx` `.doc` `.txt` `.xlsx` `.pptx` |
| Archives | `.zip` `.rar` `.7z` |
| Programs | `.exe` `.msi` |
| Python | `.py` |
| Others | everything else |

### Smart File Transfer (GUI)

- Choose files with a file dialog or drag and drop them into the window
- Choose any destination folder (created if it does not exist)
- Copies files with `shutil.copy2`, which preserves timestamps and metadata
- Live progress bar, transfer speed (MB/s) and estimated time remaining
- Pause and resume a transfer
- Renames a file (`name_<n>.ext`) instead of overwriting when the name already exists at the destination
- Runs the copy in a background thread, so the window stays responsive
- Built-in log panel

## Project Structure

```text
File-organizer/
├── file_checker.py        # CLI: sort a folder's files into category folders
├── file_transfer_ui.py    # PyQt6 app: copy files with progress, speed, ETA, pause/resume
└── FileOrganizer.spec     # PyInstaller build configuration
```

## Requirements

- Python 3.8+
- [PyQt6](https://pypi.org/project/PyQt6/) (only for the transfer app)
- [PyInstaller](https://pyinstaller.org/) (only if you want to build an executable)

`file_checker.py` uses only the Python standard library.

## Installation

```bash
git clone https://github.com/rudradevil619-byte/File-organizer.git
cd File-organizer
python -m venv .venv
```

Activate the virtual environment:

```bash
# Linux/macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

Install PyQt6 (needed for the transfer app):

```bash
pip install PyQt6
```

## Usage

### Organize a folder

```bash
python file_checker.py
```

Enter the full path of the folder when prompted:

```text
Enter folder path: C:\Users\you\Downloads
Moved: photo.jpg -> Images
Moved: report.pdf -> Documents
Moved: notes.xyz -> Others

Organization completed!
```

Only files directly inside the folder are moved. Existing subfolders are left alone.

> **Tip:** Try it on a copy of a folder first. Files are moved, not copied, and there is no undo.

### Transfer files

```bash
python file_transfer_ui.py
```

1. Click **Choose Files**, or drag files into the window.
2. Click **Choose Folder** and pick a destination.
3. Click **Start Transfer**.
4. Use **Pause Transfer** / **Resume Transfer** as needed.
5. Click **Clear** to reset the window.

## Building an Executable

The repository includes a PyInstaller spec file. With PyInstaller installed:

```bash
pip install pyinstaller
pyinstaller FileOrganizer.spec
```

The built executable appears in the `dist/` folder.

## Limitations

- `file_checker.py` moves files without confirmation, has no undo or dry-run mode, and does not handle name collisions in the destination folder.
- It is not recursive: files inside subfolders are not organized.
- Categories and extensions are hard-coded in the script.
- Pause in the transfer app takes effect between files, not in the middle of a single large file.
- The transfer app copies files only (it does not move them) and supports individual files rather than whole folders.
- **Clear** resets the window but does not cancel a transfer that is already running.

## Roadmap

- [ ] Dry-run mode and a confirmation prompt for the organizer
- [ ] Undo log for moved files
- [ ] Handle duplicate file names when organizing
- [ ] Command-line arguments (`python file_checker.py <folder>`) and a `main()` guard
- [ ] Configurable categories (JSON or YAML)
- [ ] Recursive organizing option
- [ ] Add an Organize tab to the GUI so both tools live in one app
- [ ] Real cancel button and folder support in the transfer app
- [ ] `requirements.txt` and unit tests

## Contributing

Issues and pull requests are welcome. For larger changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
