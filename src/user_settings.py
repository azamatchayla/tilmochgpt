import json
import os

DATA_FILE = "user_settings.json"

def save_user_lang(user_id, lang_code):
    data = load_data()
    data[user_id] = {"to": lang_code}
    save_data(data)

def get_user_lang(user_id):
    data = load_data()
    return data.get(user_id)

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
