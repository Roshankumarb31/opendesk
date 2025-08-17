import os
import flet as ft
from config_manager import ConfigManager
from app_launcher import AppLauncher
from startup_manager import StartupManager
from ui_manager import UIManager

def main(page: ft.Page):
    # Configuration
    config_file = os.path.expanduser("~/Documents/launcher_config.json")
    
    # Initialize managers
    config_manager = ConfigManager(config_file)
    app_launcher = AppLauncher()
    startup_manager = StartupManager()
    
    # Load configuration
    config = config_manager.load_config()
    
    # Initialize UI
    ui_manager = UIManager(page, config_manager, app_launcher, startup_manager, config)
    ui_manager.setup_ui()

if __name__ == "__main__":
    ft.app(target=main)
