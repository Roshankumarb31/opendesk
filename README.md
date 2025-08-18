![OpenDesk Logo](assets/repo_logo.png) 🚀 OpenDesk: The Ultimate Developer Launcher
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A slick, ultra-fast desktop launcher for developers—built with Python and Flet. Launch your favorite tools, terminals, and websites with a single click, all in a modern dark UI.

***

## ✨ Features

- **Multi-App Quick Launch**
  - VS Code (with project folder)
  - File Explorer (pick a directory)
  - Command Prompt & PowerShell (custom working directory)
  - Open websites in Chrome, Edge, Brave, or Firefox (normal/incognito)
  - Microsoft Teams, Outlook, MongoDB Compass, GitHub Desktop, Postman, Notepad

- **Total Customization**
  - Add, remove, enable, or disable apps as you like
  - Set custom names and icons
  - Assign browser per website item

- **Bulk Developer Actions**
  - Launch all enabled apps at once
  - Close all running developer tools with a confirmation

- **Instant Save & Restore**
  - Config auto-saved as `launcher_config.json` in your Documents

- **Polished Dark Mode**
  - Clean, focused UI for long dev sessions

***

## 🛠️ Requirements

- **Windows 10/11**
- **Python 3.7+**
- **pip install flet psutil**

***

## 📦 Installation

```bash
git clone https://github.com/Roshankumarb31/OpenDesk.git
cd OpenDesk
pip install flet psutil
python main.py
```

***

## 🎮 Usage

- **Add Launch Item:**  
  Click ➕ Add New, choose Type, set Name, pick a Path or URL, choose browser (if website), and toggle Enable.
- **Launch:**  
  Hit 🚀 Launch Selected to start all enabled tools instantly.
- **Close:**  
  Use ❌ Close All for a clean dev slate (confirmation included).
- **All settings and app lists are auto-saved.**

***

## ⚡ Supported App Types

| Type            | Description                      | Path/URL Usage (optional unless website) |
|-----------------|----------------------------------|------------------------------------------|
| VS Code         | Visual Studio Code               | Folder (project)                         |
| File Explorer   | File browser                     | Directory                                |
| Command Prompt  | Windows CMD                      | Directory                                |
| PowerShell      | Powershell terminal              | Directory                                |
| Website         | Any URL, custom browser          | Required: Website URL                    |
| Teams           | Microsoft Teams (app)            | —                                        |
| Outlook         | Microsoft Outlook (app)          | —                                        |
| MongoDB Compass | MongoDB Compass GUI              | —                                        |
| GitHub Desktop  | GitHub Desktop                   | —                                        |
| Postman         | Postman API client               | —                                        |
| Notepad         | Classic Notepad                  | —                                        |

***

## 🗂️ File Structure

```
OpenDesk/
├── main.py
├── ui_manager.py
├── app_launcher.py
├── config_manager.py
├── startup_manager.py
├── confirmation_dialogs.py
├── utils.py
├── assets/
│   └── repo_logo.jpg
├── launcher_config.json   # auto-generated
└── README.md
```

***

## ⚠️ Important

- **Windows Only:** Built exclusively for Windows desktop.
- **Safe Closing:** Only developer/launcher apps are closed, not system processes.
- **App Paths:** Common install paths auto-detected; custom installs may require tweaks.

***

## 🤝 Contributing

PRs & issues welcome! Ideas:
- More app types
- Global hotkeys
- Launcher categories/groups
- Cross-platform support

***

## 📄 License

MIT License — see [LICENSE](LICENSE).

***

> **Created with ❤️ for the dev community. Your workflow—launched in one click.**
