*** 

<p align="center"> <img src="assets/repo_logo.png" alt="OpenDesk Logo"> </p> <h1 align="center">OpenDesk — The Ultimate Developer Launcher</h1> <p align="center"> <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT"></a> <img src="https://img.shields.io/badge/Python-3.7%2B-yellow" alt="Python 3.7+"> <a href="https://flet.dev"><img src="https://img.shields.io/badge/UI-Flet-4B8CFF.svg" alt="Flet UI"></a> <a href="#-contributing"><img src="https://img.shields.io/badge/Contributions-Welcome-brightgreen" alt="Contributions Welcome"></a> </p>

### What is OpenDesk?  

**OpenDesk** is a sleek, ultra-fast desktop launcher built **for developers by developers**.  
Spin up your **favorite tools, terminals, IDEs, browsers, and websites** in seconds — all from a beautiful **dark-mode interface**.  

Think of it as your **developer control center** 🖥️. One click, and you're ready to code.  

***

## 🔥 Features  

✅ **Multi-App Quick Launch**  
- VS Code with projects  
- File Explorer at custom paths  
- Command Prompt / PowerShell in chosen directories  
- Open websites in Chrome, Edge, Brave, or Firefox (normal/incognito)  
- Teams, Outlook, MongoDB Compass, GitHub Desktop, Postman, Notepad  

✅ **Totally Customizable**  
- Add / remove apps anytime  
- Rename, re-icon, toggle enable/disable  
- Website: choose browser + incognito on/off  

✅ **One-Click Dev Environment**  
- 🚀 Launch all enabled apps  
- ❌ Close all dev tools instantly  

✅ **Smart Config**  
- Auto-saves settings into `launcher_config.json`  
- Restores your environment in seconds  

✅ **Beautiful Dark Mode**  
- Modern, clean UI designed for long coding sessions  

***

## 📂 Repository Structure  


## Repository Structure  
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
├── requirements.txt
├── app_launcher.py
├── CODE_OF_CONDUCT.md
├── config_manager.py
├── confirmation_dialogs.py
├── CONTRIBUTING.md
├── LICENSE
├── main.py
├── NOTICE
├── README.md
├── SECURITY.md
├── startup_manager.py
├── ui_manager.py
└── utils.py

```

***

## ⚡ Quick Start (Developers)  

### Requirements  
- Windows 10/11  
- Python **3.7+**  

Install dependencies:  
```bash
pip install flet psutil
```

Run locally:  
```bash
git clone https://github.com/Roshankumarb31/opendesk
cd OpenDesk
python main.py
```
Build from source (short):
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "OpenDesk_v1.0.0" --icon=assets/launcher.ico main.py
```
Full guide: see docs/build.md

***

## 📦 Pre-Built Binaries  

💡 You don’t need Python to run OpenDesk!  
Check the **[releases](./releases/)** folder for downloadable `.exe` builds.  

- Portable `.exe` → Just run and go.  
- Startup toggle → Auto-launch with Windows (optional).  

***

## 🎯 Usage  

- ➕ **Add App:** Fill type, name, path/URL, and browser if needed.  
- 🚀 **Launch Selected:** Start all checked apps.  
- ❌ **Close All:** Shut down launched dev tools.  
- 🗑️ **Delete All:** Reset your launcher setup.  

Everything is **auto-saved** — no manual config files needed.  

***

## 🤝 Open Collaboration  

This repo is meant for **community collaboration** 💡.  
We’re building OpenDesk together — for devs, by devs.  

### How to Contribute?  
1. 🍴 Fork this repo  
2. 🌱 Create a feature branch  
3. 💻 Add your improvements (new app type, UI polish, shortcuts, etc.)  
2. 🔄 Submit a Pull Request  

### Ideas to Build Together:  
- 🔑 Global hotkeys  
- 📂 App categories/groups  
- 🌍 Linux / macOS support  
- 🎨 Theme customization  
- ⏳ Better session restore  

> Your suggestions and pull requests are always welcome!  

***

## 🛡️ License  

MIT License © 2025 [Roshan Kumar B](LICENSE)  

Free to use, modify, and share.  

***

## Attribution and Branding
- OpenDesk is an open-collaboration project. Please retain original credit and license in forks and redistributions.  
- The name “OpenDesk” and the OpenDesk logo are project branding assets. Do not imply official affiliation or endorsement without permission. See assets/LOGO-LICENSE.md.

***
## ❤️ Acknowledgements  

- UI powered by [Flet](https://flet.dev)  
- System management via [psutil](https://github.com/giampaolo/psutil)  
- Inspired by devs who want their **workflow in a single click**  

> 🚀 Built with ❤️ for the developer community.  

***