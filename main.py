import time
import os
import flet as ft

# Only import essential modules at the top level
from config_manager import ConfigManager

def main(page: ft.Page):
    """Main entry point with optimized startup timing"""
    startup_timer = time.time()
    
    # ✅ LAZY IMPORTS - Import heavy modules only when needed
    from app_launcher import AppLauncher
    from startup_manager import StartupManager  
    from ui_manager import UIManager
    
    # ✅ MINIMAL CONFIGURATION SETUP
    config_file = os.path.expanduser("~/Documents/launcher_config.json")
    config_manager = ConfigManager(config_file)
    
    # ✅ LOAD CONFIG EARLY (but defer heavy processing)
    config = config_manager.load_config()
    
    # ✅ INITIALIZE MANAGERS (lightweight objects)
    app_launcher = AppLauncher()
    startup_manager = StartupManager()
    
    # ✅ SETUP UI (this is the heaviest operation)
    ui_manager = UIManager(page, config_manager, app_launcher, startup_manager, config)
    ui_manager.setup_ui()
    
    # ✅ STARTUP TIMING DEBUG INFO
    elapsed = time.time() - startup_timer
    print(f"🚀 OpenDesk launched in {elapsed:.2f} seconds")

if __name__ == "__main__":
    ft.app(target=main)
