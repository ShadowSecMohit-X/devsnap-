import json 
import os 

DATA_FILE = "snapshots.json"


def load_snapshots():
    if not  os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, dict) else {}
    except (json.JSONecoderError, OSError):
        return {}


def save_snapshots(snapshots):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(snapshots, file, indent=4)