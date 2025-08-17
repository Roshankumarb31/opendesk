import winreg as reg
import sys
import os

class StartupManager:
    def __init__(self):
        self.app_name = "OpenDesk"
        self.registry_key = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
    
    def add_to_startup(self):
        """Add the app to Windows startup registry"""
        try:
            # Get current script path - FIXED VERSION
            if getattr(sys, 'frozen', False):
                # If running as .exe
                app_path = sys.executable
            else:
                # If running as .py script, get the main.py path
                main_script = os.path.join(os.path.dirname(__file__), "main.py")
                app_path = f'python "{os.path.abspath(main_script)}"'
            
            # Open registry key
            key = reg.OpenKey(reg.HKEY_CURRENT_USER, self.registry_key, 0, reg.KEY_ALL_ACCESS)
            
            # Add our app to startup
            reg.SetValueEx(key, self.app_name, 0, reg.REG_SZ, app_path)
            reg.CloseKey(key)
            return True
        except Exception as e:
            print(f"Failed to add to startup: {e}")
            return False
    
    def remove_from_startup(self):
        """Remove the app from Windows startup"""
        try:
            key = reg.OpenKey(reg.HKEY_CURRENT_USER, self.registry_key, 0, reg.KEY_ALL_ACCESS)
            reg.DeleteValue(key, self.app_name)
            reg.CloseKey(key)
            return True
        except Exception as e:
            print(f"Failed to remove from startup: {e}")
            return False
    
    def is_in_startup(self):
        """Check if app is in startup"""
        try:
            key = reg.OpenKey(reg.HKEY_CURRENT_USER, self.registry_key, 0, reg.KEY_READ)
            reg.QueryValueEx(key, self.app_name)
            reg.CloseKey(key)
            return True
        except:
            return False
