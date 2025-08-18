***
# OpenDesk Build Guide (Windows)

This guide explains how to build OpenDesk into a portable Windows executable, manage spec files, and organize outputs for releases.

## Prerequisites

- Windows 10/11
- Python 3.7+ installed and added to PATH
- Install dependencies:
  - pip install pyinstaller
  - pip install flet psutil
- Assets:
  - Ensure assets/launcher.ico exists (for the app icon)
  - Ensure assets/repo_logo.png exists (for README and branding)

Project entry point:
- main.py

Recommended repo layout:
- assets/ (icons, branding)
- spec_files/ (PyInstaller .spec files)
- releases/ (final .exe builds)

## Quick Build (Single Command)

Produces a single-file, windowed EXE with icon.

```bash
pyinstaller --onefile --windowed --name "OpenDesk_v" --icon=assets/launcher.ico main.py
```

Outputs:
- dist/OpenDesk_v.exe → final binary
- build/ → intermediate artifacts

After building:
- Test the EXE from dist/
- Move the EXE into releases/

Examples:
- OpenDesk_v1.0.0.exe
- OpenDesk_v1.1.0.exe

## Using a .spec File (Repeatable Builds)

Generate a spec file once, then reuse it for consistent builds.

1) Generate spec

```bash
pyinstaller main.py --name OpenDesk --icon assets/launcher.ico --windowed --onefile --specpath spec_files
```

This creates: spec_files/OpenDesk.spec

2) Build from spec

```bash
pyinstaller spec_files/OpenDesk.spec
```

Advantages:
- Keep custom settings in version-controlled spec
- Easier to evolve options (data files, hidden imports, etc.)

Tip:
- If you need to bundle extra files, add them to the spec (datas=...) and rebuild.

## Versioning Best Practices

- Name the binary with a clear version: OpenDesk_vX.Y.Z.exe
- Tag releases in Git (e.g., v1.0.0)
- Update version number consistently in:
  - Release title (GitHub releases)
  - dist/ EXE name
  - Changelog (if you have one)

## Signing (Optional but Recommended)

Code-signing reduces antivirus false positives and improves trust.

- Use a code-signing certificate
- Sign after building, before placing in releases/
- Example tools: signtool (Microsoft), osslsigncode

## Common Flags Explained

- --onefile: Bundle everything into a single EXE
- --windowed: No console window
- --name: Output filename (without .exe)
- --icon: Set application icon (ICO format recommended)

## Troubleshooting

- EXE doesn’t start:
  - Rebuild without --windowed to see console errors
  - Ensure Python version is compatible (3.7+)
  - Confirm dependencies installed: flet, psutil

- Icon not applied:
  - Confirm assets/launcher.ico path
  - ICO must be a valid .ico (not .png renamed)

- Antivirus flags EXE:
  - Add dist/ to local exclusions for testing
  - Prefer signed builds for public releases
  - Avoid bundling unnecessary files

- Missing assets at runtime:
  - If referencing external files at runtime, ensure paths exist
  - For bundling data, use .spec (datas=...) and rebuild

## Release Checklist

- [ ] Update version number in build command or spec
- [ ] Build and smoke test the EXE locally
- [ ] Place final EXE under releases/ (e.g., releases/OpenDesk_v1.0.0.exe)
- [ ] Update README if anything user-facing changed
- [ ] Create/update Git tag and GitHub release
- [ ] Optionally attach SHA256 checksum

## Optional: Quick Build Script (Windows)

Create scripts/build.bat to automate versioned builds:

```bat
@echo off
setlocal

if "%~1"=="" (
  echo Usage: build.bat ^
  echo Example: build.bat 1.0.0
  exit /b 1
)

set VERSION=%~1
set NAME=OpenDesk_v%VERSION%

echo Building %NAME% ...
pyinstaller --onefile --windowed --name "%NAME%" --icon=assets/launcher.ico main.py

if exist "dist\%NAME%.exe" (
  if not exist "releases" mkdir releases
  copy /Y "dist\%NAME%.exe" "releases\%NAME%.exe"
  echo Build complete: releases\%NAME%.exe
) else (
  echo Build failed. Check the logs above.
  exit /b 1
)

endlocal
```

Usage:
```bash
scripts\build.bat 1.0.0
```

This builds and copies the final EXE to releases/.

***