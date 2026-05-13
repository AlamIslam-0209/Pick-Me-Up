# mengambil data dari heroBlueprints.json
import json
path = 'd:\\Coding\\Projek Akhir DSA\\Pick Me Up\\'
with open(path + 'data\\heroBlueprints.json', 'r') as f:
    hero_data = json.load(f)

# 1. Buat rak Hash Table dengan ukuran 50
database_katalog = HashTable(50)

# 2. Masukkan data (blueprint) karakter ke dalam Hash Table
for hero_id, hero_info in hero_data.items():
    database_katalog.tambah(hero_id, hero_info)

# 3. Saat pemain Gacha dan butuh memanggil hero, 
# program tidak perlu mencari satu-satu. Langsung panggil ID-nya!
hasil_pencarian = database_katalog.cari("H004")

print(f"Data ditemukan: {hasil_pencarian['name']} (Bintang {ha