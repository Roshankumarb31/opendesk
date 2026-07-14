import os
import json
import shutil

DEFAULT_THEME = {
    "bg": "#16171C",
    "surface": "#21222A",
    "primary": "#4B8CFF",
    "accent": "#FFD952",
    "danger": "#FF4B7A",
    "gray": "#23242B",
    "text": "#ECECF1",
    "subtext": "#FFFFFF"
}

DEFAULT_CONFIG = {
    "version": 2,
    "launch_items": [],
    "theme": dict(DEFAULT_THEME),
    "settings": {
        "terminal_profile": "auto",
        "file_manager": "auto"
    }
}

class ConfigManager:
    def __init__(self, config_path):
        self.config_path = config_path

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    data = json.load(f)
                if data.get("version") != 2:
                    data = self._migrate(data)
                data.setdefault("theme", dict(DEFAULT_THEME))
                data.setdefault("settings", {"terminal_profile": "auto", "file_manager": "auto"})
                data.setdefault("launch_items", [])
                return data
            except Exception as e:
                print(f"Error loading config: {e}")
        return dict(DEFAULT_CONFIG)

    def _migrate(self, data):
        new_data = {"version": 2, "launch_items": data.get("launch_items", []),
                    "theme": dict(DEFAULT_THEME),
                    "settings": {"terminal_profile": "auto", "file_manager": "auto"}}
        return new_data

    def save_config(self, config):
        try:
            config["version"] = 2
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False

    def add_item(self, config, item):
        config.setdefault("launch_items", []).append(item)
        return self.save_config(config)

    def remove_item(self, config, index):
        if 0 <= index < len(config.get("launch_items", [])):
            del config["launch_items"][index]
            return self.save_config(config)
        return False

    def export_config(self, export_path):
        try:
            shutil.copy2(self.config_path, export_path)
            return True
        except Exception as e:
            print(f"Error exporting config: {e}")
            return False

    def import_config(self, import_path):
        try:
            with open(import_path, 'r') as f:
                data = json.load(f)
            data.setdefault("launch_items", [])
            return data
        except Exception as e:
            print(f"Error importing config: {e}")
            return None
