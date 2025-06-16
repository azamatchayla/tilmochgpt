import json
import os

SETTINGS_FILE = "user_lang.json"

# Sozlamani saqlash
def save_user_lang(user_id, to_lang):
    settings = load_settings()
    settings[user_id] = {"to": to_lang}
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)

# Sozlamani yuklash
def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {}
    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# O‘qish
def get_user_lang(user_id):
    settings = load_settings()
    return settings.get(user_id, {"to": "uz"})  # Default: uz