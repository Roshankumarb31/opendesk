import os
import json

class ConfigManager:
    def __init__(self, config_path):
        self.config_path = config_path
        
    def load_config(self):
        """Load saved configuration from JSON file"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
        return {"launch_items": []}
    
    def save_config(self, config):
        """Save current configuration to JSON file"""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def add_item(self, config, item):
        """Add new launch item to config"""
        if "launch_items" not in config:
            config["launch_items"] = []
        config["launch_items"].append(item)
        return self.save_config(config)
    
    def remove_item(self, config, index):
        """Remove launch item from config"""
        if 0 <= index < len(config.get("launch_items", [])):
            del config["launch_items"][index]
            return self.save_config(config)
        return False
