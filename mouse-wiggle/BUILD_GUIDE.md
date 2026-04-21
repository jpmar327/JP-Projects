# 🖱️ Mouse Wiggler — Build Guide

This guide walks you through building Mouse Wiggler on **Windows** and **macOS**, either locally on your machine or automatically via GitHub Actions.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Build on Windows](#build-on-windows)
3. [Build on macOS](#build-on-macos)
4. [Build Both via GitHub Actions (No Mac Required)](#build-both-via-github-actions)
5. [Distributing Your Builds](#distributing-your-builds)
6. [Packaging Background](#packaging-background)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Make sure you have these two source files in the same folder:
- `gui.py`
- `move_cursor.py`

Both platforms require **Python 3.8 or later**:
- **Windows**: Download from [python.org](https://www.python.org/downloads/) — check "Add Python to PATH" during install
- **macOS**: Download from [python.org](https://www.python.org/downloads/) or run `python3 --version` in Terminal to check if it's already installed

This project uses **PyInstaller** to build the executable. PyInstaller bundles your Python app and all its dependencies into a single file that anyone can run without installing Python. Learn more at the [PyInstaller documentation](https://pyinstaller.org/en/stable/).

> **Note:** This project previously used PyOxidizer as the build tool, which required Rust to be installed and was significantly more complex to set up. PyInstaller was chosen as a simpler, more reliable alternative. If you're curious about PyOxidizer, see the [PyOxidizer documentation](https://pyoxidizer.readthedocs.io).

---

## Build on Windows

### Step 1 — Open PowerShell

Open **PowerShell** and navigate to your project folder:

```powershell
cd C:\Users\jpmar\Documents\GitHub\JP-Projects\mouse-wiggle
```

### Step 2 — Install Dependencies

Install all required packages. The full list of dependencies is:
- `pyinstaller` — bundles the app into an executable
- `pyautogui` — controls the mouse

```powershell
pip install pyinstaller pyautogui
```

### Step 3 — Build the Executable

```powershell
pyinstaller --onefile --windowed --name "Mouse-Wiggler" gui.py
```

This will take a minute or two. When finished, your app will be at:

```
dist\Mouse-Wiggler.exe
```

> **About the generated files:** PyInstaller also creates a `Mouse-Wiggler.spec` file and a `build\` folder during this process. These are temporary working files. The `.spec` file is a configuration recipe PyInstaller uses — it will be recreated automatically next time you build. Both the `.spec` file and `build\` folder can be safely deleted after a successful build.

### Step 4 — Run the App

Double-click `Mouse-Wiggler.exe` in the `dist\` folder, or run:

```powershell
.\dist\Mouse-Wiggler.exe
```

### ⚠️ Windows SmartScreen Warning

The first time someone runs the app they may see a "Windows protected your PC" warning. This is normal for apps that aren't signed with a code signing certificate.

To get past it:
1. Click **More info**
2. Click **Run anyway**

> Code signing certificates eliminate this warning but cost $200–$500/year. For personal or internal use, the "Run anyway" workaround is fine. Learn more at [Microsoft's documentation on SmartScreen](https://learn.microsoft.com/en-us/windows/security/operating-system-security/virus-and-threat-protection/microsoft-defender-smartscreen/).

---

## Build on macOS

> **Important:** PyInstaller can only build for the OS it's running on. You cannot build a macOS app from Windows. If you don't have a Mac, use the [GitHub Actions method](#build-both-via-github-actions) below instead.

### Step 1 — Open Terminal

Open **Terminal** (press `Cmd + Space` and search for Terminal).

Navigate to your project folder:

```bash
cd ~/Desktop/mouse-wiggle
```

### Step 2 — Install Dependencies

```bash
pip3 install pyinstaller pyautogui
```

### Step 3 — Build the App

```bash
pyinstaller --onefile --windowed --name "Mouse-Wiggler" gui.py
```

When finished, your app will be at:

```
dist/Mouse-Wiggler.app
```

> **About the generated files:** Same as Windows — PyInstaller creates a `Mouse-Wiggler.spec` file and `build\` folder that can both be deleted after a successful build.

### Step 4 — Run the App

Double-click `Mouse-Wiggler.app` in Finder, or run:

```bash
open dist/Mouse-Wiggler.app
```

### ⚠️ macOS Gatekeeper Warning

If macOS says the app can't be opened because it's from an unidentified developer:

1. Right-click (or Control-click) the app
2. Select **Open**
3. Click **Open** in the dialog

This is a one-time step for apps not signed with an Apple Developer certificate. Learn more at [Apple's Gatekeeper documentation](https://support.apple.com/en-us/102445).

### ⚠️ macOS Accessibility Permission

Because the app controls the mouse, macOS will block it until you grant permission:

1. Go to **System Settings → Privacy & Security → Accessibility**
2. Click the **+** button and add **Mouse-Wiggler**
3. Make sure the toggle is **ON**

Then try opening the app again. This is a one-time setup.

---

## Build Both via GitHub Actions

If you don't have a Mac (or want builds to happen automatically), GitHub Actions can build both versions for free in the cloud every time you push code. This replaces the need for any local build scripts.

> **What is GitHub Actions?** It's a free CI/CD service built into GitHub that runs automated tasks on virtual machines in the cloud. Learn more at the [GitHub Actions documentation](https://docs.github.com/en/actions).

### Step 1 — Create the Workflow File

In your repo, create this file and folder path:

```
.github/workflows/build.yml
```

### Step 2 — Paste This Workflow

```yaml
name: Build Mouse Wiggler

on:
  push:
    branches: [main]

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install pyinstaller pyautogui

      - name: Build executable
        run: pyinstaller --onefile --windowed --name "Mouse-Wiggler" gui.py

      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: Mouse-Wiggler-Windows
          path: dist/Mouse-Wiggler.exe

  build-macos:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip3 install pyinstaller pyautogui

      - name: Build app
        run: pyinstaller --onefile --windowed --name "Mouse-Wiggler" gui.py

      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: Mouse-Wiggler-macOS
          path: dist/Mouse-Wiggler
```

### Step 3 — Push to GitHub

```bash
git add .github/workflows/build.yml
git commit -m "Add Windows and macOS build workflow"
git push
```

### Step 4 — Download Your Builds

1. Go to your GitHub repo
2. Click the **Actions** tab
3. Click the latest workflow run
4. Scroll down to **Artifacts**
5. Download **Mouse-Wiggler-Windows** or **Mouse-Wiggler-macOS**

---

## Distributing Your Builds

The best way to share both versions is via **GitHub Releases**:

1. Go to your repo on GitHub
2. Click **Releases → Create a new release**
3. Upload both `Mouse-Wiggler.exe` (Windows) and `Mouse-Wiggler.app` (macOS)
4. Include this note in the release description:

   > **Windows users:** If SmartScreen blocks the app, click "More info" then "Run anyway."
   >
   > **macOS users:** Right-click the app and select Open the first time you run it. You will also need to grant Accessibility permissions under System Settings → Privacy & Security → Accessibility.

Learn more about creating GitHub Releases at the [GitHub Releases documentation](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository).

---

## Packaging Background

Packaging converts Python source code into a standalone app that anyone can run without installing Python or any dependencies. The general process looks like this:

```
Python Source Code + Python Runtime + Dependencies
           ↓
    PyInstaller
           ↓
    Single Executable File (.exe / .app)
```

This project uses **PyInstaller** because it works on both Windows and macOS, requires no additional tools, and produces a reliable single-file executable. For more advanced packaging options, see the [Python Packaging User Guide](https://packaging.python.org).

---

## File Summary

| File | Purpose |
|---|---|
| `gui.py` | Main app — same source file for both platforms |
| `move_cursor.py` | Mouse movement logic — required by `gui.py` |
| `requirements.txt` | Lists pip dependencies for running from source (`pyautogui`) |
| `README.md` | Project overview and quick start instructions |
| `BUILD_GUIDE.md` | This file — build and distribution instructions |
| `dist/Mouse-Wiggler.exe` | Built Windows app |
| `dist/Mouse-Wiggler.app` | Built macOS app |
| `.github/workflows/build.yml` | Optional — automates both builds on GitHub |

---

## Troubleshooting

**`pyinstaller` not found (Windows)**
```powershell
python -m PyInstaller --onefile --windowed --name "Mouse-Wiggler" gui.py
```

**`pyinstaller` not found (macOS)**
```bash
python3 -m PyInstaller --onefile --windowed --name "Mouse-Wiggler" gui.py
```

**`pyautogui` install fails on macOS**
```bash
pip3 install pyautogui --break-system-packages
```

**App crashes immediately on launch (macOS)**

Run it from Terminal to see the error output:
```bash
./dist/Mouse-Wiggler
```

**App crashes immediately on launch (Windows)**

Run it from PowerShell to see the error output:
```powershell
.\dist\Mouse-Wiggler.exe
```

**Need more help?**
- [PyInstaller documentation](https://pyinstaller.org/en/stable/)
- [pyautogui documentation](https://pyautogui.readthedocs.io)
- [GitHub Actions documentation](https://docs.github.com/en/actions)
