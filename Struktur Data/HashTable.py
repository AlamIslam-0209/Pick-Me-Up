class HashTable():
    def __init__(self, ukuran):
        self.ukuran = ukuran
        self.table = [None] * ukuran

    def _fungsiHash(self, key):
        total = 0

        for huruf in key:
            total += ord(huruf)

        return total % self.ukuran
    
    def tambah(self, key, value):
        indeks = self._fungsiHash(key)

        if self.table[indeks] is None:
            self.table[indeks] = []

        self.table[indeks].append((key, value))

    def cari(self, key):
        indeks = self._fungsiHash(key)

        if self.table[indeks] is not None:
            for pasangan in self.table[indeks]:
                if pasangan[0] == key:
                    return pasangan[1]

        return None


# # mengambil data dari heroBlueprints.json
# import json
# path = 'd:\\Coding\\Projek Akhir DSA\\Pick Me Up\\'
# with open(path + 'data\\heroBlueprints.json', 'r') as f:
#     hero_data = json.load(f)

# # 1. Buat rak Hash Table dengan ukuran 50
# database_katalog = HashTable(50)

# # 2. Masukkan data (blueprint) karakter ke dalam Hash Table
# for hero_id, hero_info in hero_data.items():
#     database_katalog.tambah(hero_id, hero_info)

# # 3. Saat pemain Gacha dan butuh memanggil hero, 
# # program tidak perlu mencari satu-satu. Langsung panggil ID-nya!
# hasil_pencarian = database_katalog.cari("H004")

# print(f"Data ditemukan: {hasil_pencarian['name']} (Bintang {hasil_pencarian['star_level']})")

