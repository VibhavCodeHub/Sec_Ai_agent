import json
import os

def load_config():
    import json
    import os
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    return {"voice_enabled": False, "admin_mode": True, "wake_word": "mayra", "hotkey": "ctrl+shift+m"}

