import json
from pathlib import Path


def save_game(path, state_dict):
    """Simpan state game ke file JSON. `path` bisa berupa str atau Path."""
    p = Path(path) 
    p.parent.mkdir(parents=True, exist_ok=True) 
    with open(p, "w") as f:
        json.dump(state_dict, f, indent=4) 


def load_game(path):
    """Muat state game dari file JSON. Mengembalikan dict atau {} jika tidak ada."""
    p = Path(path)
    if not p.exists():
        return {}

    with open(p, "r") as f:
        return json.load(f)
