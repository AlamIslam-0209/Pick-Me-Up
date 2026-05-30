import json
from pathlib import Path


def save_game(path, state_dict):
    """Menyimpan kemajuan (progress) permainan saat ini ke dalam file JSON."""
    p = Path(path) 
    p.parent.mkdir(parents=True, exist_ok=True) 
    with open(p, "w") as f:
        json.dump(state_dict, f, indent=4) 


def load_game(path):
    """Memuat data permainan dari file JSON. Mengembalikan data kosong jika file tidak ditemukan."""
    p = Path(path)
    if not p.exists():
        return {}

    with open(p, "r") as f:
        return json.load(f)
