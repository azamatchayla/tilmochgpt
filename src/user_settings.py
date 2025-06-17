import json
import os

# Foydalanuvchi sozlamalari saqlanadigan fayl
SETTINGS_FILE = "user_settings.json"

# Fayl mavjud bo‘lmasa, bo‘sh dict bilan yaratish
if not os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f)

# Tilni saqlash
def save_user_lang(user_id, to_lang):
    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        settings = json.load(f)

    settings[user_id] = {"to": to_lang}

    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4, ensure_ascii=False)

# Saqlangan tilni olish
def get_user_lang(user_id):
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            settings = json.load(f)
        return settings.get(user_id, {"to": "uz"})  # Default: o‘zbekcha
    except Exception:
        return {"to": "uz"}
