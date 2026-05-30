import json
import random

tema_musuh = {
    "Hutan Pemula": ["M01", "M02", "M03"],            
    "Gua Lembap": ["M04", "M05", "M06", "M07"],       
    "Padang Rumput Angin": ["M08", "M09", "M10"],     
    "Reruntuhan Kuno": ["M11", "M12", "M13"],         
    "Kastil Terbengkalai": ["M14", "M15", "M16"],     
    "Gurun Pasir Panas": ["M17", "M18", "M19"],       
    "Oasis Tersembunyi": ["M20", "M21"],              
    "Lembah Racun": ["M22", "M23", "M24"],            
    "Hutan Berbisik": ["M25", "M26"],                 
    "Pegunungan Es": ["M27", "M28", "M29"],           
    "Kuil Beku": ["M28", "M29", "M30"],               
    "Danau Kaca": ["M31", "M32"],                     
    "Gunung Berapi": ["M33", "M34", "M35"],           
    "Lautan Lahar": ["M35", "M36", "M37"],            
    "Gua Kristal": ["M38", "M39", "M40"],             
    "Jembatan Langit": ["M41", "M42"],                
    "Pulau Terapung": ["M43", "M44"],                 
    "Dimensi Kesengsaraan": ["M45", "M46", "M47"],    
    "Kuil Bintang": ["M48", "M49"],                   
    "Istana Langit": ["M50", "M51", "M52"]            
}

def generate_blueprint_tower(file_path):
    data_tower = []
    lantai_counter = 1
    
    # Ada 20 tema. Setiap tema = 5 lantai. Total 100 lantai.
    for idx, (nama_lokasi, pool_musuh) in enumerate(tema_musuh.items()):
        for i in range(1, 6):
            is_boss = (i == 5)
            
            if not is_boss:
                jumlah_musuh = random.randint(2, 5)
                pasukan = random.choices(pool_musuh, k=jumlah_musuh)
            else:
                id_boss = f"BOSS_{idx + 1:02d}"
                jumlah_minions = random.randint(1, 3)
                minions = random.choices(pool_musuh, k=jumlah_minions)
                pasukan = [id_boss] + minions
                
            lantai = {
                "no_lantai": lantai_counter,
                "nama_lokasi": nama_lokasi,
                "is_boss": is_boss,
                "id_musuh": pasukan
            }
            data_tower.append(lantai)
            lantai_counter += 1

    with open(file_path, 'w') as file:
        json.dump(data_tower, file, indent=4)
        
    print(f"[*] Menghasilkan blueprint tower ({len(data_tower)} Lantai).")

if __name__ == "__main__":
    generate_blueprint_tower("blueprint_tower.json")
