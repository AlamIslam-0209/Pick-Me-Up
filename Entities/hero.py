from Entities.entity import Entity

class Hero(Entity):
    def __init__(self, data_dict):
        # Mengambil data dari JSON (HashTable)
        # super() memanggil __init__ dari class Entity
        super().__init__(
            nama=data_dict.get("name", "Unknown Hero"),
            hp=data_dict.get("hp", 100),
            attack=data_dict.get("attack", 10),
            level=data_dict.get("level", 1)
        )
        
        # Atribut khusus Hero
        self.id = data_dict.get("id", "H000")
        self.star_level = data_dict.get("star_level", 1)
        self.max_level = self.star_level * 20
        self.equipment = data_dict.get("equipment", {})
        self.exp = 0
        self.exp_next = self.level * 100 
        self.is_exploring = False

    def tambah_xp(self, xp_tambahan):
        """Dipanggil di main.py setelah menang raid"""
        if not self.is_alive:
            return
            
        self.exp += xp_tambahan
        print(f"✨ {self.nama} mendapat {xp_tambahan} EXP! ({self.exp}/{self.exp_next})")
        
        while self.exp >= self.exp_next and self.level < self.max_level:
            self.exp -= self.exp_next
            self.level_up()
            self.exp_next = self.level * 100

    def pesan_kematian(self):
        print(f"{str(self.nama).capitalize()}[{'⭐' * self.star_level}] TELAH KEMBALI KE PELUKAN SANG DEWI! Semangat juangnya akan selalu dikenang selamanya")

    def level_up(self):
        """Fungsi internal saat XP memenuhi syarat"""
        if not self.is_alive:
            print(f"[!] Tidak bisa menaikkan level {self.nama} karena ia sudah gugur!")
            return False

        if self.level < self.max_level:
            self.level += 1
            
            pertumbuhan_hp = self.star_level * 10
            pertumbuhan_atk = self.star_level * 5
            
            self.hp_max += pertumbuhan_hp
            self.hp += pertumbuhan_hp 
            self.attack += pertumbuhan_atk

            print(f"🌟 LEVEL UP! {self.nama} naik ke Lv.{self.level}!")
            print(f"   [+] HP Max  : +{pertumbuhan_hp} (Total: {self.hp_max})")
            print(f"   [+] Attack  : +{pertumbuhan_atk} (Total: {self.attack})")
            return True
        else:
            print(f"[!] {self.nama} sudah mencapai batas Max Level (Lv.{self.max_level}) untuk {self.star_level}⭐!")
            print("    Butuh Evolusi (Naik Bintang) untuk bisa level up lagi.")
            return False
        
    def dapat_evolusi(self):
        """Cek apakah hero sudah bisa evolusi (naik bintang)"""
        return self.level >= self.max_level and self.star_level < 7

    def evolusi(self):
        """Menaikkan bintang hero jika sudah mencapai max level"""
        if not self.dapat_evolusi():
            return
        self.star_level += 1
        self.max_level = self.star_level * 20
        print("\n" + "="*40)
        print(f"✨ EVOLUSI BERHASIL! ✨")
        print(f"{self.nama} menembus batas dan naik menjadi {self.star_level}⭐!")
        print(f"Batas Level meningkat menjadi Lv.{self.max_level}!")
        print("="*40 + "\n")
        return

    def tampilkan_stats(self):
        """Dipanggil di main.py saat melihat Daftar Hero di Barrack"""
        senjata = self.equipment.get('weapon', 'Tangan Kosong')
        status_nyawa = "HIDUP" if self.is_alive else "GUGUR"
        
        print(f"[{self.id}] {self.nama} ({"⭐" * self.star_level}) | Lv.{self.level}")
        print(f"    Status: {status_nyawa} | HP: {self.hp}/{self.hp_max} | ATK: {self.attack}")
        print(f"    Senjata: {senjata}")
        print("    " + "-"*35)

    def to_dict(self):
        """Fungsi tambahan untuk Teman A (Algoritma/save_load.py) jika ingin di-save"""
        return {
            "id": self.id,
            "name": self.nama,
            "star_level": self.star_level,
            "level": self.level,
            "hp": self.hp_max,
            "attack": self.attack,
            "equipment": self.equipment,
            "status_effects": {}
        }
        
    
    