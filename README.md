*** 

<p align="center"> <img src="assets/repo_logo.png" alt="OpenDesk Logo"> </p> <h1 align="center">OpenDesk — The Ultimate Developer Launcher</h1> <p align="center"> <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT"></a> <img src="https://img.shields.io/badge/Python-3.7%2B-yellow" alt="Python 3.7+"> <a href="https://flet.dev"><img src="https://img.shields.io/badge/UI-Flet-4B8CFF.svg" alt="Flet UI"></a> <a href="#-contributing"><img src="https://img.shields.io/badge/Contributions-Welcome-brightgreen" alt="Contributions Welcome"></a> <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-blue" alt="Windows | Linux"> <br> <a href="https://github.com/Roshankumarb31/opendesk/releases/latest"><img src="https://img.shields.io/github/v/release/Roshankumarb31/opendesk?label=Download&color=4B8CFF" alt="Download"></a> <img src="https://img.shields.io/badge/Windows-.exe-blue?logo=windows" alt="Windows .exe"> <img src="https://img.shields.io/badge/Linux-Binary-orange?logo=linux" alt="Linux Binary"> </p>

### What is OpenDesk?  

**OpenDesk** is a sleek, cross-platform desktop launcher built **for developers by developers**.  
Spin up your **favorite tools, terminals, IDEs, browsers, and websites** in seconds — all from a beautiful **dark-mode interface**.  

Think of it as your **developer control center** 🖥️. One click, and you're ready to code.  

***

## 🔥 Features  

### 🚀 App Launcher  
- VS Code with project paths  
- File Explorer / File Manager at custom paths  
- Command Prompt / PowerShell / Terminal in chosen directories  
- Open websites in Chrome, Edge, Brave, or Firefox (normal/incognito)  
- Teams, Outlook, MongoDB Compass, GitHub Desktop, Postman, Notepad  
- **Custom App** — add ANY executable or binary (Windows .exe or Linux binary)  

### ⌨️ Command Palette  
- Press **Ctrl+Space** to open a quick-search popup  
- Type to search across all apps  
- Hit Enter to launch instantly — no need to open the full UI  

### 📂 App Groups / Workspaces  
- Assign a group tag to each app (e.g., "Dev", "Personal", "Design")  
- Filter the list by group  
- Launch all apps in a group at once  

### 🎨 Theme Customization  
- Fully customizable color scheme (8 theme colors)  
- Change bg, surface, primary, accent, danger, text, and more  
- Reset to default with one click  
- Settings saved per-profile  

### 📦 Portable Mode  
- Drop `launcher_config.json` next to the executable  
- OpenDesk automatically detects and uses it as the config source  
- No config in user home needed — truly portable  

### 💾 Import / Export Config  
- **Export** — save your launcher setup as a JSON file  
- **Import** — load config from another machine (Replace or Merge)  
- Share your workflow across devices  

### 🔧 Cross-Platform (Windows + Linux)  
- **Windows**: Registry startup, native EXE icons, full app support  
- **Linux**: `.desktop` autostart, emoji icons, detects `gnome-terminal`/`konsole`/`xfce4-terminal`/`alacritty`/`kitty`, `xdg-open` for files  
- Terminal profile setting to pick your preferred terminal  
- File manager setting to pick nautilus/nemo/thunar/dolphin  

### ⚡ One-Click Dev Environment  
- 🚀 Launch all enabled apps at once  
- ❌ Close all dev tools instantly  
- Toggle auto-launch at startup  

### 👟 Smart Config  
- Auto-saves settings into `launcher_config.json`  
- Portable mode: save config next to the app  
- Versioned config schema (auto-migrates old configs)  

***

## 📥 Download  

### Windows
- **Portable `.exe`** — download from [GitHub Releases](https://github.com/Roshankumarb31/opendesk/releases/latest)
- No installation needed — just run the `.exe`
- Config saves to `~/Documents/launcher_config.json` (or next to the `.exe` for portable mode)

### Linux  
- **Standalone binary** — download from [GitHub Releases](https://github.com/Roshankumarb31/opendesk/releases/latest)
- Make executable: `chmod +x OpenDesk_*_linux && ./OpenDesk_*_linux`
- Config saves to `~/.config/opendesk/launcher_config.json`

> Binaries are auto-built by GitHub Actions on every release. No Python required.

***

## 📂 Repository Structure  

## 📂 Repository Structure  

```bash
OpenDesk/
├── assets/                   # Logos, icons, branding
│   ├── launcher.ico
│   ├── LOGO-LICENSE.md
│   └── repo_logo.png
│
├── docs/                     # Documentation
│   └── build.md
│
├── releases/                 # Pre-built .exe releases
│   └── OpenDesk_v*.exe
│
├── spec_files/               # PyInstaller spec files
│   └── *.spec
│
├── .github/                  # GitHub templates
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md
│       └── feature_request.md
│
├── .gitignore
├── app_launcher.py
├── CODE_OF_CONDUCT.md
├── config_manager.py
├── confirmation_dialogs.py
├── CONTRIBUTING.md
├── LICENSE
├── main.py
├── NOTICE
├── platform_adapter.py       # Cross-platform abstraction layer
├── README.md
├── requirements.txt
├── SECURITY.md
├── startup_manager.py
├── ui_manager.py
└── utils.py
```

***

## ⚡ Quick Start  

### 🖥️ Pre-built Binaries (Recommended)
Download the latest `.exe` (Windows) or binary (Linux) from **[GitHub Releases](https://github.com/Roshankumarb31/opendesk/releases/latest)** — no Python needed.

### 🐍 Run from Source  
**Requirements:** Python **3.7+**  

```bash
git clone https://github.com/Roshankumarb31/opendesk
cd OpenDesk
pip install -r requirements.txt
python main.py          # Windows
python3 main.py         # Linux
```

### 📦 Build Your Own Executable  
```bash
pip install pyinstaller
# Windows
pyinstaller --onefile --windowed --name "OpenDesk_v1.0.0" --icon=assets/launcher.ico main.py
# Linux
pyinstaller --onefile --name "OpenDesk_v1.0.0" main.py
```
> Releases are auto-built by GitHub Actions — just push a `v*` tag and both Windows `.exe` and Linux binary are generated automatically.

***

## 🎯 Usage  

| Feature | How |
|---|---|
| ➕ **Add App** | Click "+ Add New" button, choose type, set name/path |
| 🔍 **Search** | Type in search bar to filter apps |
| ⌨️ **Command Palette** | Press `Ctrl+Space`, type app name, press Enter |
| 🚀 **Launch All** | Click "Launch All" to start all enabled apps |
| 📂 **Groups** | Type a group name in the "Group" field on any row, then filter by group dropdown |
| 🎨 **Theme** | Click gear icon → Settings → edit colors |
| 💾 **Import/Export** | Use Import/Export buttons in action bar |
| ❌ **Close All** | Kill all launched dev processes |
| 🗑️ **Delete All** | Reset your launcher setup |
| 🏠 **Portable Mode** | Place `launcher_config.json` next to the executable |
| ⚙️ **Terminal/File Mgr** | Settings dialog → choose preferred terminal/file manager |

Everything is **auto-saved** — no manual config files needed.  

***

## 🤝 Open Collaboration  

This repo is meant for **community collaboration** 💡.  
We're building OpenDesk together — for devs, by devs.  

### How to Contribute?  
1. 🍴 Fork this repo  
2. 🌱 Create a feature branch  
3. 💻 Add your improvements  
4. 🔄 Submit a Pull Request  

> Your suggestions and pull requests are always welcome!  

***

## 🛡️ License  

MIT License © 2025 [Roshan Kumar B](LICENSE)  

Free to use, modify, and share.  

***

## Attribution and Branding
- OpenDesk is an open-collaboration project. Please retain original credit and license in forks and redistributions.  
- The name "OpenDesk" and the OpenDesk logo are project branding assets. Do not imply official affiliation or endorsement without permission. See assets/LOGO-LICENSE.md.

***
## ❤️ Acknowledgements  

- UI powered by [Flet](https://flet.dev)  
- System management via [psutil](https://github.com/giampaolo/psutil)  
- Inspired by devs who want their **workflow in a single click**  

> 🚀 Built with ❤️ for the developer community.  

***
