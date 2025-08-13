# 🚀 Simple Developer Launcher

A lightweight desktop application built with Python and Flet that helps developers quickly launch their favorite tools, applications, and websites from a single, customizable interface.

## ✨ Features

- **Multi-App Support**: Launch various developer tools including:
  - VS Code (with optional project path)
  - File Explorer (with optional directory)
  - Command Prompt & PowerShell (with optional working directory)
  - Web browsers (Chrome, Edge, Brave, Firefox) with custom URLs
  - Microsoft Teams & Outlook
  - MongoDB Compass
  - GitHub Desktop
  - Postman
  - Notepad

- **Customizable Launch Items**: 
  - Add/remove launch items dynamically
  - Enable/disable items without deleting them
  - Set custom names and paths for each item
  - Choose specific browsers for website launches

- **Bulk Operations**:
  - Launch all enabled items with one click
  - Close all running applications with confirmation dialog

- **Persistent Configuration**: Settings are automatically saved to `launcher_config.json`

- **Dark Theme**: Easy on the eyes with a modern dark interface

## 🛠️ Requirements

- Python 3.7+
- Required packages:
  ```
  flet
  psutil
  ```

## 📦 Installation

1. Clone or download this repository
2. Install the required dependencies:
   ```bash
   pip install flet psutil
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## 🎯 Usage

### Adding Launch Items

1. Click the **"➕ Add New Item"** button
2. Configure your item:
   - **Type**: Select the application type from the dropdown
   - **Name**: Give your item a custom name
   - **Path/URL**: 
     - For applications: Optional path to open in that location
     - For websites: The URL to open
   - **Browser**: (Websites only) Choose which browser to use
   - **Enabled**: Check/uncheck to enable/disable the item

### Launching Applications

- Click **"🚀 Launch Selected"** to launch all enabled items
- Items launch in the background, allowing you to continue working

### Closing Applications

1. Click **"❌ Close All"** to access the close confirmation page
2. Review the warning and confirm your choice
3. The app will close all supported running applications

### Configuration

The application automatically saves your configuration to `launcher_config.json` in the same directory. This file contains all your launch items and their settings.

## 🎨 Interface Overview

The main interface consists of:
- **Header**: Application title and navigation
- **Control Buttons**: Launch, Close All, and Add New Item actions
- **Items List**: Scrollable list of all configured launch items
- **Status Bar**: Shows the current application status

## 🔧 Supported Applications

| Application Type | Description | Path Usage |
|-----------------|-------------|------------|
| VS Code | Opens Visual Studio Code | Optional: Project folder to open |
| File Explorer | Opens Windows File Explorer | Optional: Directory to navigate to |
| Command Prompt | Opens Windows CMD | Optional: Working directory |
| PowerShell | Opens Windows PowerShell | Optional: Working directory |
| Website | Opens URL in specified browser | Required: Website URL |
| Teams | Opens Microsoft Teams | N/A |
| Outlook | Opens Microsoft Outlook | N/A |
| MongoDB Compass | Opens MongoDB Compass | N/A |
| GitHub Desktop | Opens GitHub Desktop | N/A |
| Postman | Opens Postman API client | N/A |
| Notepad | Opens Windows Notepad | N/A |

## 📁 File Structure

```
simple-developer-launcher/
├── main.py                 # Main application file
├── launcher_config.json    # Configuration file (auto-generated)
└── README.md              # This file
```

## ⚠️ Important Notes

- **Windows Only**: This application is designed for Windows systems
- **Administrator Rights**: Some operations may require administrator privileges
- **Application Paths**: The app attempts to find applications in common installation directories
- **Safe Closing**: The close function only targets specific developer applications and won't close system-critical processes

## 🤝 Contributing

Feel free to fork this project and submit pull requests for improvements. Some ideas for enhancements:
- Support for additional applications
- Cross-platform compatibility
- Custom application paths
- Keyboard shortcuts
- Application grouping/categories

## 📄 License

This project is open source and available under the MIT License.

***

**Built with ❤️ using Python and Flet**