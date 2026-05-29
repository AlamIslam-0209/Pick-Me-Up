class Entity:
    def __init__(self, nama, hp, attack, level=1):
        self.nama = nama
        self.hp_max = hp
        self.hp = hp
        self.attack = attack
        self.level = level
        self.is_alive = True

    def serang(self, target):
        """Method menyerang yang dipanggil di Combat.py"""
        print(f"⚔️ {self.nama} menyerang {target.nama} sebesar {self.attack} DMG!")
        target.terima_damage(self.attack)

    def terima_damage(self, damage):
        """Method internal untuk mengurangi HP dan cek kematian"""
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.is_alive = False
            print(f"💀 {self.nama} telah GUGUR di medan pertempuran!")

    def pulihkan_kondisi(self):
        """Dipanggil di main.py setelah menang raid untuk me-reset HP hero"""
        if self.is_alive:
            self.hp = self.hp_max
