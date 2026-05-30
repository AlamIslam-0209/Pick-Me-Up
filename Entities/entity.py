class Entity:
    def __init__(self, nama, hp, attack, level=1):
        self.nama = nama
        self.hp = hp
        self.hp_max = hp
        self.attack = attack
        self.level = level
        self.is_alive = True
        
    def pesan_kematian(self):
        pass

    def terima_damage(self, damage):
        """
        Mengurangi HP karakter sesuai dengan jumlah damage yang diterima. 
        Jika HP habis, karakter dianggap mati dan memicu pesan kematian.
        """
        if not self.is_alive:
            return

        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.is_alive = False
            self.pesan_kematian()

    def serang(self, target):
        """
        Melakukan serangan ke entitas target.
        Karakter dan target harus sama-sama dalam keadaan hidup agar serangan berhasil.
        """
        if self.is_alive and target.is_alive:
            print(f"      {self.nama} memberikan {self.attack} DMG kepada {target.nama}!")
            target.terima_damage(self.attack)