import os
import sys
import platform
import subprocess

SYSTEM = platform.system()
VERSION = "1.0.0"

APP_INSTALL_PATHS = {
    "MongoDB Compass": {
        "Windows": [
            f"C:\\Users\\{os.environ.get('USERNAME', '')}\\AppData\\Local\\MongoDBCompass\\MongoDBCompass.exe",
            "C:\\Program Files\\MongoDB Compass\\MongoDBCompass.exe"
        ],
        "Linux": ["/usr/bin/mongodb-compass", "/snap/bin/mongodb-compass"]
    },
    "GitHub Desktop": {
        "Windows": [
            f"C:\\Users\\{os.environ.get('USERNAME', '')}\\AppData\\Local\\GitHubDesktop\\GitHubDesktop.exe",
            "C:\\Program Files\\GitHub Desktop\\GitHubDesktop.exe"
        ],
        "Linux": ["/usr/bin/github-desktop", "/snap/bin/github-desktop"]
    },
    "Postman": {
        "Windows": [
            f"C:\\Users\\{os.environ.get('USERNAME', '')}\\AppData\\Local\\Postman\\Postman.exe",
            "C:\\Program Files\\Postman\\Postman.exe"
        ],
        "Linux": ["/usr/bin/postman", "/snap/bin/postman"]
    }
}

def get_script_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def get_config_path():
    portable = os.path.join(get_script_dir(), "launcher_config.json")
    if os.path.exists(portable):
        return portable
    if SYSTEM == "Windows":
        return os.path.expanduser("~/Documents/launcher_config.json")
    return os.path.expanduser("~/.config/opendesk/launcher_config.json")

def get_app_paths(app_type):
    return APP_INSTALL_PATHS.get(app_type, {}).get(SYSTEM, [])


def _get_app_executable():
    if getattr(sys, 'frozen', False):
        return sys.executable
    main_script = os.path.join(os.path.dirname(__file__), "main.py")
    if SYSTEM == "Windows":
        return f'python "{os.path.abspath(main_script)}"'
    return f'python3 "{os.path.abspath(main_script)}"'


def is_in_startup():
    if SYSTEM == "Windows":
        return _windows_is_in_startup()
    return _linux_is_in_startup()

def add_to_startup():
    if SYSTEM == "Windows":
        return _windows_add_to_startup()
    return _linux_add_to_startup()

def remove_from_startup():
    if SYSTEM == "Windows":
        return _windows_remove_from_startup()
    return _linux_remove_from_startup()

def _windows_is_in_startup():
    import winreg as reg
    try:
        key = reg.OpenKey(reg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run", 0, reg.KEY_READ)
        reg.QueryValueEx(key, "OpenDesk")
        reg.CloseKey(key)
        return True
    except:
        return False

def _windows_add_to_startup():
    import winreg as reg
    try:
        key = reg.OpenKey(reg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run", 0, reg.KEY_ALL_ACCESS)
        reg.SetValueEx(key, "OpenDesk", 0, reg.REG_SZ, _get_app_executable())
        reg.CloseKey(key)
        return True
    except Exception as e:
        print(f"Failed to add to startup: {e}")
        return False

def _windows_remove_from_startup():
    import winreg as reg
    try:
        key = reg.OpenKey(reg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run", 0, reg.KEY_ALL_ACCESS)
        reg.DeleteValue(key, "OpenDesk")
        reg.CloseKey(key)
        return True
    except Exception as e:
        print(f"Failed to remove from startup: {e}")
        return False

def _linux_is_in_startup():
    return os.path.exists(os.path.expanduser("~/.config/autostart/opendesk.desktop"))

def _linux_add_to_startup():
    autostart_dir = os.path.expanduser("~/.config/autostart")
    os.makedirs(autostart_dir, exist_ok=True)
    desktop_entry = f"""[Desktop Entry]
Type=Application
Name=OpenDesk
Exec={_get_app_executable()}
Terminal=false
Categories=Utility;
X-GNOME-Autostart-enabled=true
"""
    with open(os.path.join(autostart_dir, "opendesk.desktop"), "w") as f:
        f.write(desktop_entry)
    return True

def _linux_remove_from_startup():
    path = os.path.expanduser("~/.config/autostart/opendesk.desktop")
    if os.path.exists(path):
        os.remove(path)
        return True
    return False


ICON_MAP = {
    "VS Code": "💻", "File Explorer": "📂", "Command Prompt": "🖥️",
    "PowerShell": "⚡", "Teams": "👥", "Outlook": "📧",
    "MongoDB Compass": "🍃", "GitHub Desktop": "🐙",
    "Postman": "📬", "Notepad": "📝", "Website": "🌐",
    "Custom App": "📎"
}
FALLBACK_ICON = "❓"

def get_app_icon(app_type, custom_path=None):
    if app_type == "Custom App" and custom_path and os.path.exists(custom_path):
        if SYSTEM == "Windows":
            icon = _extract_exe_icon(custom_path)
            if icon:
                return icon
        return "📎"
    if SYSTEM == "Windows":
        return _windows_get_icon(app_type)
    return _linux_get_icon(app_type)

def _extract_exe_icon(exe_path):
    import win32ui, win32gui, win32con
    from PIL import Image
    import tempfile
    try:
        large, small = win32gui.ExtractIconEx(exe_path, 0)
        if large:
            hicon = large[0]
            hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
            hbmp = win32ui.CreateBitmap()
            hbmp.CreateCompatibleBitmap(hdc, 64, 64)
            hdc = hdc.CreateCompatibleDC()
            hdc.SelectObject(hbmp)
            win32gui.DrawIconEx(hdc.GetHandleOutput(), 0, 0, hicon, 64, 64, 0, None, win32con.DI_NORMAL)
            bmpinfo = hbmp.GetInfo()
            bmpstr = hbmp.GetBitmapBits(True)
            img = Image.frombuffer("RGBA", (bmpinfo["bmWidth"], bmpinfo["bmHeight"]), bmpstr, "raw", "BGRA", 0, 1)
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            img.save(tmp.name, "PNG")
            return tmp.name
    except Exception as e:
        print(f"Icon extract failed for {exe_path}: {e}")
    return None

def _windows_get_icon(app_type):
    import win32ui, win32gui, win32con
    from PIL import Image
    import tempfile
    exe_map = {
        "VS Code": "Code.exe", "File Explorer": "explorer.exe",
        "Command Prompt": "cmd.exe", "PowerShell": "powershell.exe",
        "Teams": "ms-teams.exe", "Outlook": "olk.exe",
        "MongoDB Compass": "MongoDBCompass.exe",
        "GitHub Desktop": "GitHubDesktop.exe",
        "Postman": "Postman.exe", "Notepad": "Notepad.exe",
    }
    exe_name = exe_map.get(app_type)
    if not exe_name:
        return ICON_MAP.get(app_type, FALLBACK_ICON)
    for path_dir in os.environ.get("PATH", "").split(os.pathsep):
        exe_path = os.path.join(path_dir, exe_name)
        if os.path.exists(exe_path):
            icon = _extract_exe_icon(exe_path)
            if icon:
                return icon
    return ICON_MAP.get(app_type, FALLBACK_ICON)

def _linux_get_icon(app_type):
    return ICON_MAP.get(app_type, FALLBACK_ICON)


def which(program):
    for path_dir in os.environ.get("PATH", "").split(os.pathsep):
        exe_file = os.path.join(path_dir, program)
        if os.path.isfile(exe_file) and os.access(exe_file, os.X_OK):
            return True
    return False


TERMINAL_COMMANDS = {
    "gnome-terminal": {"linux": "gnome-terminal", "args_workdir": ["--working-directory"]},
    "konsole": {"linux": "konsole", "args_workdir": ["--workdir"]},
    "xfce4-terminal": {"linux": "xfce4-terminal", "args_workdir": ["--working-directory"]},
    "lxterminal": {"linux": "lxterminal", "args_workdir": ["--working-directory"]},
    "xterm": {"linux": "xterm", "args_workdir": ["-e", "cd {path} && exec bash"]},
    "alacritty": {"linux": "alacritty", "args_workdir": ["--working-directory"]},
    "kitty": {"linux": "kitty", "args_workdir": ["--working-directory"]},
    "Windows Terminal": {"windows": "wt", "args_cd": ["-d"]},
}

def detect_available_terminals():
    terminals = []
    if SYSTEM == "Windows":
        if which("wt"):
            terminals.append("Windows Terminal")
        terminals.extend(["Command Prompt", "PowerShell"])
    else:
        for name, info in TERMINAL_COMMANDS.items():
            if "linux" in info and which(info["linux"]):
                terminals.append(name)
        if not terminals:
            terminals.append("xterm")
    return terminals

def detect_available_file_managers():
    if SYSTEM == "Windows":
        return ["File Explorer"]
    fms = []
    for fm in ["nautilus", "nemo", "thunar", "pcmanfm", "dolphin"]:
        if which(fm):
            fms.append(fm)
    if not fms:
        fms.append("xdg-open")
    return fms

def launch_vscode(path=""):
    cmd = ["code"]
    if path and os.path.exists(path):
        cmd = ["code", path]
    subprocess.Popen(cmd, shell=(SYSTEM == "Windows"))

def launch_explorer(path="", file_manager="auto"):
    if SYSTEM == "Windows":
        cmd = ["explorer"]
        if path and os.path.exists(path):
            cmd = ["explorer", path]
        subprocess.Popen(cmd, shell=True)
    else:
        if file_manager == "auto" or not file_manager:
            for fm in ["nautilus", "nemo", "thunar", "pcmanfm", "dolphin"]:
                if which(fm):
                    file_manager = fm
                    break
            if file_manager == "auto":
                file_manager = "xdg-open"
        target = path if path and os.path.exists(path) else os.path.expanduser("~")
        subprocess.Popen([file_manager, target])

def launch_terminal(terminal_type="auto", path=""):
    if SYSTEM == "Windows":
        if terminal_type == "Windows Terminal" and which("wt"):
            cmd = ["wt"]
            if path and os.path.exists(path):
                cmd.extend(["-d", path])
            subprocess.Popen(cmd)
        else:
            if path and os.path.exists(path):
                subprocess.Popen(f'start cmd /k "cd /d {path}"', shell=True)
            else:
                subprocess.Popen("start cmd", shell=True)
    else:
        if terminal_type == "auto" or not terminal_type:
            for name in ["gnome-terminal", "konsole", "xfce4-terminal", "lxterminal", "xterm"]:
                if which(name):
                    terminal_type = name
                    break
            else:
                terminal_type = "xterm"
        info = TERMINAL_COMMANDS.get(terminal_type)
        if info and which(info["linux"]):
            args = [info["linux"]]
            if path and os.path.exists(path):
                if terminal_type == "xterm":
                    args.extend(["-e", f"cd {path} && exec bash"])
                elif terminal_type == "kitty":
                    args.extend(["--working-directory", path])
                elif terminal_type == "alacritty":
                    args.extend(["--working-directory", path])
                else:
                    args.extend(["--working-directory", path])
            subprocess.Popen(args)
        else:
            subprocess.Popen(["xterm"])

def launch_browser(browser, incognito=False, url=""):
    if SYSTEM == "Windows":
        flags = {"chrome": "--incognito", "edge": "--inprivate", "brave": "--incognito", "firefox": "--private-window"}
        browsers = {"chrome": "chrome", "edge": "msedge", "brave": "brave", "firefox": "firefox"}
        b = browsers.get(browser, "chrome")
        cmd = ["start", b]
        if incognito and b in flags:
            cmd.append(flags[b])
        if url:
            cmd.append(url)
        subprocess.Popen(cmd, shell=True)
    else:
        browsers = {"chrome": "google-chrome", "edge": "microsoft-edge", "brave": "brave-browser", "firefox": "firefox"}
        b = browsers.get(browser, "xdg-open")
        cmd = [b]
        if incognito:
            incognito_flags = {"google-chrome": "--incognito", "microsoft-edge": "--inprivate",
                               "brave-browser": "--incognito", "firefox": "--private-window"}
            if b in incognito_flags:
                cmd.append(incognito_flags[b])
        if url:
            cmd.append(url)
        try:
            subprocess.Popen(cmd)
        except FileNotFoundError:
            subprocess.Popen(["xdg-open", url] if url else ["xdg-open", ""])

def launch_teams():
    subprocess.Popen(["xdg-open", "ms-teams:"] if SYSTEM != "Windows" else ["start", "ms-teams:"], shell=(SYSTEM == "Windows"))

def launch_outlook():
    try:
        subprocess.Popen(["xdg-open", "outlookmail:"] if SYSTEM != "Windows" else ["start", "outlookmail:"], shell=(SYSTEM == "Windows"))
    except Exception:
        subprocess.Popen(["xdg-open", "outlook"] if SYSTEM != "Windows" else ["start", "outlook"], shell=(SYSTEM == "Windows"))

def launch_notepad():
    if SYSTEM == "Windows":
        subprocess.Popen(["notepad"], shell=True)
    else:
        for editor in ["gedit", "kate", "mousepad", "xed", "nano", "vim"]:
            if which(editor):
                subprocess.Popen([editor])
                return
        subprocess.Popen(["gedit"])

def launch_custom_app(path):
    if path and os.path.exists(path):
        subprocess.Popen([path], shell=(SYSTEM == "Windows"))
        return True
    return False

def launch_app_by_paths(paths, fallback_name):
    for p in paths:
        if os.path.exists(p):
            subprocess.Popen([p], shell=(SYSTEM == "Windows"))
            return True
    if SYSTEM == "Windows":
        subprocess.Popen(["start", fallback_name], shell=True)
    return False


PROCESS_NAMES = {
    "Windows": [
        "Code.exe", "explorer.exe", "cmd.exe", "powershell.exe",
        "chrome.exe", "msedge.exe", "brave.exe", "firefox.exe",
        "notepad.exe", "Notepad.exe", "notepad++.exe",
        "Teams.exe", "OUTLOOK.EXE", "MongoDBCompass.exe",
        "GitHubDesktop.exe", "Postman.exe", "olk.exe", "ms-teams.exe"
    ],
    "Linux": [
        "code", "nautilus", "nemo", "thunar", "gnome-terminal",
        "konsole", "xfce4-terminal", "google-chrome", "chromium",
        "microsoft-edge", "brave-browser", "firefox",
        "gedit", "kate", "mousepad",
        "teams", "mongodb-compass", "github-desktop", "postman"
    ]
}
