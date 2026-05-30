from .entity import Entity

class Hero(Entity):
    def __init__(self, data_dict):
        super().__init__(
            nama = data_dict['name'],
            hp = data_dict['hp'],
            attack = data_dict['attack'],
            level = data_dict.get('level', 1)
        )
        self.id = data_dict['id']
        self.star_level = data_dict['star_level']
        self.is_exploring = False
        self.weapon = data_dict['equipment']['weapon']
        self.max_level = self.star_level * 20
        
        self.exp = 0
        self.exp_next = self.level * 100 
        
    def pesan_kematian(self):
        """
        Menampilkan teks saat hero gugur dalam pertarungan.
        """
        print(f"{str(self.nama).capitalize()}[{'⭐' * self.star_level}] TELAH KEMBALI KE PELUKAN SANG DEWI! Semangat juangnya akan selalu dikenang selamanya")
    
    def pulihkan_kondisi(self):
        """
        Memulihkan HP hero hingga kembali penuh (Max HP). Digunakan setelah menyelesaikan satu lantai.
        """
        if self.is_alive:
            self.hp = self.hp_max
            
            
    def tambah_xp(self, jumlah):
        """
        Menambahkan poin EXP (pengalaman) ke hero. 
        Jika jumlah EXP melebihi batas yang dibutuhkan, hero akan otomatis naik level.
        """
        if not self.is_alive:
            return
        
        self.exp += jumlah
        while self.exp >= self.exp_next and self.level < self.max_level:
            self.exp -= self.exp_next
            self.level_up()
            self.exp_next = self.level * 100
        

    def level_up(self):
        """
        Meningkatkan status batas HP dan Attack hero setiap kali naik level.
        Hero tidak dapat naik level lagi jika sudah menyentuh batas maksimal dari bintangnya.
        """
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

    def evolusi(self):
        """
        Meningkatkan jumlah bintang hero agar batas level maksimalnya terbuka kembali.
        Batas tertinggi untuk evolusi hero adalah 7 bintang.
        """
        if self.star_level >= 7:
            print(f"[!] {self.nama} sudah mencapai batas kelangkaan tertinggi (7⭐)!")
            return False
            
        if self.level < self.max_level:
            print(f"[!] Evolusi gagal! {self.nama} harus mencapai Lv.{self.max_level} terlebih dahulu.")
            return False
            
        self.star_level += 1
        self.max_level = self.star_level * 20
        
        print("\n" + "="*40)
        print(f"✨ EVOLUSI BERHASIL! ✨")
        print(f"{self.nama} menembus batas dan naik menjadi {self.star_level}⭐!")
        print(f"Batas Level meningkat menjadi Lv.{self.max_level}!")
        print("="*40 + "\n")
        return True

    def tampilkan_stats(self):
        """Menampilkan ringkasan informasi, status kesehatan, dan senjata yang digunakan hero."""
        status = "Hidup" if self.is_alive else "GUGUR"
        print(f"[{self.star_level}⭐] {self.nama} (Lv.{self.level}/{self.max_level}) - {status}")
        print(f"    Senjata: {self.weapon} | HP: {self.hp}/{self.hp_max} | ATK: {self.attack}")