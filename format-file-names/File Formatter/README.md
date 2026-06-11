# Film Formatter

A desktop app for organizing and renaming files from a DSLR SD card.

DSLR cameras write photos across multiple numbered folders (e.g. `102D3100`, `103D3100`) with repeating file names in each. Copying them all into one folder causes overwrites. Film Formatter solves this by scanning all source subfolders, grouping same-shot files (e.g. `.jpg` + `.nef` with the same base name in the same folder), and renaming them into a clean sequential structure organized by file type.

---

## Output Structure

Given a prefix of `JP_Film`, month `6`, and year `2026`, the output looks like:

```
<source_folder>/
└── Formatted/
    ├── jpg/
    │   ├── JP_Film_6_2026_00001.jpg
    │   ├── JP_Film_6_2026_00002.jpg
    │   └── ...
    └── nef/
        ├── JP_Film_6_2026_00001.nef
        ├── JP_Film_6_2026_00002.nef
        └── ...
```

Files from the same shot (same stem, same source folder) share the same number across formats. The counter increments only when a new unique shot is encountered.

---

## Project Structure

```
film_formatter/
├── main.py     # Entry point — run this to launch the app
├── gui.py      # Tkinter GUI — all visual logic
├── core.py     # Business logic — file scanning, rename planning, copy, delete
└── README.md   # This file
```

`core.py` has no GUI dependencies and can be imported independently for scripting or testing.

---

## Requirements

- Python 3.10 or newer
- Tkinter (included with most Python installations)

### Tkinter installation (if missing)

**macOS:**
```bash
brew install python-tk
```

**Linux (Debian/Ubuntu):**
```bash
sudo apt install python3-tk
```

**Windows:** Tkinter is bundled with the official Python installer from python.org. Make sure the "tcl/tk and IDLE" option is checked during installation.

---

## Running the App

```bash
cd film_formatter
python main.py
```

---

## Building a Standalone Executable

Use [PyInstaller](https://pyinstaller.org) to package the app into a single executable that runs without a Python installation.

### Install PyInstaller

```bash
pip install pyinstaller
```

---

### Windows — build a `.exe`

```bash
pyinstaller --onefile --windowed --name "FilmFormatter" main.py
```

Output: `dist/FilmFormatter.exe`

To include a custom icon (`.ico` format):
```bash
pyinstaller --onefile --windowed --name "FilmFormatter" --icon icon.ico main.py
```

---

### macOS — build a `.app`

```bash
pyinstaller --onefile --windowed --name "FilmFormatter" main.py
```

Output: `dist/FilmFormatter.app`

To include a custom icon (`.icns` format):
```bash
pyinstaller --onefile --windowed --name "FilmFormatter" --icon icon.icns main.py
```

To allow the app to run on macOS without a security warning, you can ad-hoc sign it:
```bash
codesign --force --deep --sign - dist/FilmFormatter.app
```

---

### Linux — build a binary

```bash
pyinstaller --onefile --name "FilmFormatter" main.py
```

Output: `dist/FilmFormatter`

Make it executable:
```bash
chmod +x dist/FilmFormatter
./dist/FilmFormatter
```

> **Note:** Linux builds are not `--windowed` because that flag suppresses the terminal, which is unnecessary on Linux and can interfere with some display environments.

---

### Build output

After any build, PyInstaller creates:

```
film_formatter/
├── build/          # Intermediate build files (safe to delete)
├── dist/           # Final executable lives here
└── FilmFormatter.spec   # Build spec (can be reused with: pyinstaller FilmFormatter.spec)
```

To rebuild from the spec file without retyping all flags:
```bash
pyinstaller FilmFormatter.spec
```

---

## Delete Originals Feature

After formatting completes, if **"Offer to delete original source folders"** is checked, the app will pause and display an inline confirmation bar listing every source folder that would be removed.

The deletion flow requires **two confirmations**:

1. Click **"Yes, delete folders"** or **"No, keep originals"** in the app
2. A system dialog asks **"Are you sure?"** before any action is taken

Clicking "No" to keeping files returns you to the first prompt. Nothing is deleted unless both confirmations pass. Deletion removes the entire source subfolder tree (e.g. `102D3100/`), not individual files.

---

## Notes

- The app copies files — originals are never touched unless you explicitly confirm deletion.
- Folder processing order follows the filesystem's `os.listdir()` order, which matches the original script's behavior. File numbering reflects this order.
- Re-running the formatter into an existing `Formatted/` folder will overwrite files with the same output names. Clear the `Formatted/` folder between runs if needed.
