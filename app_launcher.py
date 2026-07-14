import os
import psutil
from platform_adapter import (
    SYSTEM, launch_vscode, launch_explorer, launch_terminal,
    launch_browser, launch_teams, launch_outlook,
    launch_notepad, launch_custom_app, launch_app_by_paths,
    get_app_paths, PROCESS_NAMES
)

class AppLauncher:
    def launch_item(self, item):
        try:
            app_type = item["type"]
            if app_type == "VS Code":
                launch_vscode(item.get("path", ""))
            elif app_type == "File Explorer":
                launch_explorer(item.get("path", ""), item.get("file_manager", "auto"))
            elif app_type == "Command Prompt":
                launch_terminal("Command Prompt", item.get("path", ""))
            elif app_type == "PowerShell":
                launch_terminal("PowerShell", item.get("path", ""))
            elif app_type == "Website":
                self._launch_website(item)
            elif app_type == "Teams":
                launch_teams()
            elif app_type == "Outlook":
                launch_outlook()
            elif app_type == "MongoDB Compass":
                launch_app_by_paths(get_app_paths("MongoDB Compass"), "MongoDB Compass")
            elif app_type == "GitHub Desktop":
                launch_app_by_paths(get_app_paths("GitHub Desktop"), "Github Desktop")
            elif app_type == "Postman":
                launch_app_by_paths(get_app_paths("Postman"), "Postman")
            elif app_type == "Notepad":
                launch_notepad()
            elif app_type == "Custom App":
                return launch_custom_app(item.get("path", ""))
            else:
                return False
            return True
        except Exception as e:
            print(f"Error launching {item.get('name', 'unknown')}: {e}")
            return False

    def _launch_website(self, item):
        url = item.get("path", "").strip()
        browser = item.get("browser", "chrome")
        incognito = item.get("incognito", False)
        if url and not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        launch_browser(browser, incognito, url)

    def launch_group(self, items):
        launched = 0
        for item in items:
            if item.get("enabled", True) and self.launch_item(item):
                launched += 1
        return launched

    def get_enabled_items(self, config):
        return [i for i in config.get("launch_items", []) if i.get("enabled", True)]

    def close_all_windows(self):
        closed_count = 0
        targets = PROCESS_NAMES.get(SYSTEM, PROCESS_NAMES["Windows"])
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                proc_name = proc.info['name']
                if proc_name in targets:
                    if proc_name in ("explorer.exe", "nautilus", "nemo", "thunar"):
                        if len(proc.children()) > 0:
                            proc.terminate()
                            closed_count += 1
                    else:
                        proc.terminate()
                        closed_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return closed_count
