import os
import win32ui
import win32gui
import win32con
from PIL import Image
import tempfile

class AppIcons:
    """Fetch real icons from installed apps, fallback to emojis if not found"""

    # Map app type → known executable name
    EXE_MAP = {
        "VS Code": "Code.exe",
        "File Explorer": "explorer.exe",
        "Command Prompt": "cmd.exe",
        "PowerShell": "powershell.exe",
        "Teams": "ms-teams.exe",
        "Outlook": "olk.exe",
        "MongoDB Compass": "MongoDBCompass.exe",
        "GitHub Desktop": "GitHubDesktop.exe",
        "Postman": "Postman.exe",
        "Notepad": "Notepad.exe",
        "Website": None
    }

    # Fallback emoji icons (used when EXE icon cannot be extracted)
    ICON_MAP = {
        "VS Code": "💻",
        "File Explorer": "📂",
        "Command Prompt": "🖥️",
        "PowerShell": "⚡",
        "Teams": "👥",
        "Outlook": "📧",
        "MongoDB Compass": "🍃",
        "GitHub Desktop": "🐙",
        "Postman": "📬",
        "Notepad": "📝",
        "Website": "🌐"
    }

    FALLBACK_ICON = "❓"

    @classmethod
    def get_icon(cls, app_type):
        exe_name = cls.EXE_MAP.get(app_type)
        # If no exe defined, return fallback emoji
        if not exe_name:
            return cls.ICON_MAP.get(app_type, cls.FALLBACK_ICON)

        # Try to find executable in PATH
        for path in os.environ["PATH"].split(os.pathsep):
            exe_path = os.path.join(path, exe_name)
            if os.path.exists(exe_path):
                icon_path = cls.extract_icon(exe_path)
                if icon_path:  # success
                    return icon_path

        # If exe not found or extract failed → fallback to emoji
        return cls.ICON_MAP.get(app_type, cls.FALLBACK_ICON)

    @staticmethod
    def extract_icon(exe_path):
        """Extract first icon from exe → return temp PNG path, else None"""
        try:
            large, small = win32gui.ExtractIconEx(exe_path, 0)
            if large:
                hicon = large[0]
                hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
                hbmp = win32ui.CreateBitmap()
                hbmp.CreateCompatibleBitmap(hdc, 64, 64)
                hdc = hdc.CreateCompatibleDC()
                hdc.SelectObject(hbmp)
                win32gui.DrawIconEx(
                    hdc.GetHandleOutput(), 0, 0, hicon, 64, 64, 0, None, win32con.DI_NORMAL
                )

                bmpinfo = hbmp.GetInfo()
                bmpstr = hbmp.GetBitmapBits(True)
                img = Image.frombuffer(
                    "RGBA",
                    (bmpinfo["bmWidth"], bmpinfo["bmHeight"]),
                    bmpstr,
                    "raw",
                    "BGRA",
                    0,
                    1,
                )
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
                img.save(tmp.name, "PNG")
                return tmp.name
        except Exception as e:
            print(f"Icon extract failed for {exe_path}: {e}")
        return None  # fail → return None
