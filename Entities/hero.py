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
        self.equipment = data_dict.get("equipment", {})
        self.xp = 0

    def tambah_xp(self, xp_tambahan):
        """Dipanggil di main.py setelah menang raid"""
        if not self.is_alive:
            return  # Hero mati tidak dapat XP
            
        self.xp += xp_tambahan
        xp_dibutuhkan = self.level * 100  # Rumus simpel: Lv 1 butuh 100, Lv 2 butuh 200
        
        print(f"✨ {self.nama} mendapat {xp_tambahan} EXP! ({self.xp}/{xp_dibutuhkan})")
        
        if self.xp >= xp_dibutuhkan:
            self.level_up(xp_dibutuhkan)

    def pesan_kematian(self):
        print(f"{str(self.nama).capitalize()}[{'⭐' * self.star_level}] TELAH KEMBALI KE PELUKAN SANG DEWI! Semangat juangnya akan selalu dikenang selamanya")

    def level_up(self, xp_dibutuhkan):
        """Fungsi internal saat XP memenuhi syarat"""
        self.xp -= xp_dibutuhkan
        self.level += 1
        
        # Naik stat
        tambahan_hp = 15
        tambahan_atk = 3
        
        self.hp_max += tambahan_hp
        self.attack += tambahan_atk
        self.hp = self.hp_max # Heal full saat level up
        
        print(f"🎉 LEVEL UP! {self.nama} naik ke Level {self.level} (HP +{tambahan_hp}, ATK +{tambahan_atk})")

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
    
    