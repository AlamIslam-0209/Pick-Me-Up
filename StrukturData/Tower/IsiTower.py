import json
import random
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
json_path = ROOT_DIR / "data"

def buat_blueprint_menara():

    tema_menara = [
        "Hutan Pemula", "Gua Lembap", "Padang Rumput Angin", "Reruntuhan Kuno", "Kastil Terbengkalai",
        "Gurun Pasir Panas", "Oasis Tersembunyi", "Lembah Racun", "Hutan Berbisik", "Pegunungan Es",
        "Kuil Beku", "Danau Kaca", "Gunung Berapi", "Lautan Lahar", "Gua Kristal",
        "Jembatan Langit", "Pulau Terapung", "Dimensi Kesengsaraan", "Kuil Bintang", "Istana Langit"
    ]
    
    data_menara = []
    
    boss_counter = 1 

    for i in range(1, 101):
        indeks_tema = (i - 1) // 5
        tema_sekarang = tema_menara[indeks_tema]
        
        is_boss_stage = (i % 5 == 0)
        
        if is_boss_stage:
            id_musuh = f"BOSS_{boss_counter:02d}" 
            boss_counter += 1 
        else:
            id_musuh = f"M{random.randint(1, 30):02d}" 
        
        lantai = {
            "no_lantai": i,
            "nama_lokasi": tema_sekarang,
            "is_boss": is_boss_stage,
            "id_musuh": id_musuh
        }
        
        data_menara.append(lantai)

    with open( json_path / "blueprint_tower.json", "w") as file:
        json.dump(data_menara, file, indent=4)
        
    print("Selesai! 100 lantai dengan 20 Tema Bioma dan 20 Boss Unik telah dibuat.")

buat_blueprint_menara()
