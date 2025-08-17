import os

class AppIcons:
    """Icon mapping for different app types"""
    ICON_MAP = {
        "VS Code": "🆚",
        "File Explorer": "📁",
        "Command Prompt": "💻",
        "PowerShell": "🔷",
        "Website": "🌐",
        "Teams": "👥",
        "Outlook": "📧",
        "MongoDB Compass": "🍃",
        "GitHub Desktop": "🐙",
        "Postman": "📮",
        "Notepad": "📝"
    }
    
    @classmethod
    def get_icon(cls, app_type):
        return cls.ICON_MAP.get(app_type, "⚙️")

def validate_path(path):
    """Validate if a path exists"""
    if not path:
        return False
    return os.path.exists(path.strip())

def format_path_display(path, max_length=50):
    """Format path for display with ellipsis if too long"""
    if not path:
        return "Default location"
    
    if len(path) <= max_length:
        return path
    
    return f"...{path[-(max_length-3):]}"
