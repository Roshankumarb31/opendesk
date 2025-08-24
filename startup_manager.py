import subprocess
import sys
import os
import winreg as reg

class StartupManager:
    def __init__(self):
        self.app_name = "OpenDesk"
        self.registry_key = r"Software\Microsoft\Windows\CurrentVersion\Run"

    def get_app_path(self):
        """Get the correct path to launch the application"""
        if getattr(sys, 'frozen', False):
            # If running as .exe
            return sys.executable
        else:
            # If running as .py script
            main_script = os.path.join(os.path.dirname(__file__), "main.py")
            return f'python "{os.path.abspath(main_script)}"'

    # NEW: Task Scheduler methods for fastest startup
    def add_startup_task(self):
        """Create a scheduled task for immediate startup after login"""
        try:
            cmd = [
                'schtasks', '/create', '/f',  # /f forces overwrite if exists
                '/tn', self.app_name,
                '/tr', self.get_app_path(),
                '/sc', 'onlogon',           # Trigger: at user logon
                '/rl', 'highest',           # Run with highest privileges
                '/delay', '0000:00'         # No delay - start immediately
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to create scheduled task: {e}")
            return False
        except Exception as e:
            print(f"Error creating startup task: {e}")
            return False

    def remove_startup_task(self):
        """Remove the scheduled task"""
        try:
            subprocess.run([
                'schtasks', '/delete', 
                '/tn', self.app_name, 
                '/f'  # Force delete without confirmation
            ], check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError:
            # Task might not exist
            return True  
        except Exception as e:
            print(f"Error removing startup task: {e}")
            return False

    def is_startup_task_exists(self):
        """Check if scheduled task exists"""
        try:
            result = subprocess.run([
                'schtasks', '/query', '/tn', self.app_name
            ], capture_output=True, text=True)
            return result.returncode == 0 and self.app_name in result.stdout
        except Exception:
            return False

    # LEGACY: Keep registry methods as fallback
    def add_to_startup(self):
        """Add the app to Windows startup registry (fallback method)"""
        try:
            app_path = self.get_app_path()
            key = reg.OpenKey(reg.HKEY_CURRENT_USER, self.registry_key, 0, reg.KEY_ALL_ACCESS)
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
        """Check if app is in startup (checks both task scheduler and registry)"""
        return self.is_startup_task_exists() or self._is_in_registry()
    
    def _is_in_registry(self):
        """Check if app is in registry startup"""
        try:
            key = reg.OpenKey(reg.HKEY_CURRENT_USER, self.registry_key, 0, reg.KEY_READ)
            reg.QueryValueEx(key, self.app_name)
            reg.CloseKey(key)
            return True
        except:
            return False
