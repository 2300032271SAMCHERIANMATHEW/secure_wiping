import json
import os
from pathlib import Path

# Define default config (works across all OS)
DEFAULT_CONFIG = {
    "overwrite_method": "random",   # overwrite strategy
    "passes": 3,                    # how many times to overwrite
    "logging": True,                # enable/disable logging
    "log_file": "deletion.log",     # default log file
    "confirmation_required": True   # ask before wiping
}

class ConfigManager:
    def __init__(self, config_path="config.json"):
        self.config_path = Path(config_path)
        self.config = self.load_config()

    def load_config(self):
        """Load config.json if exists, else create with defaults."""
        if self.config_path.exists():
            try:
                with open(self.config_path, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("⚠️ Config corrupted. Resetting to defaults.")
                return self.reset_config()
        else:
            return self.reset_config()

    def reset_config(self):
        """Reset to defaults and save."""
        self.config = DEFAULT_CONFIG.copy()
        self.save_config()
        return self.config

    def save_config(self):
        """Write config to file safely (cross-platform)."""
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=4)

    def update_option(self, key, value):
        """Update a single option dynamically."""
        if key in DEFAULT_CONFIG:
            self.config[key] = value
            self.save_config()
        else:
            print(f"⚠️ Unknown option: {key}")

    def get_option(self, key):
        """Fetch a config option safely."""
        return self.config.get(key, DEFAULT_CONFIG.get(key))
