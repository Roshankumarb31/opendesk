import flet as ft
from config_manager import ConfigManager
from app_launcher import AppLauncher
from startup_manager import StartupManager
from ui_manager import UIManager
from platform_adapter import get_config_path, VERSION

def main(page: ft.Page):
    config_manager = ConfigManager(get_config_path())
    app_launcher = AppLauncher()
    startup_manager = StartupManager()
    config = config_manager.load_config()
    ui_manager = UIManager(page, config_manager, app_launcher, startup_manager, config)
    ui_manager.setup_ui()

if __name__ == "__main__":
    ft.app(target=main)
