from Entities.entity import Entity
import random

class Enemy(Entity):
    def __init__(self, nama, hp, atk, is_boss=False):
        super().__init__(nama=nama, hp=hp, attack=atk)
        
        self.is_boss = is_boss

    def serang(self, target):
        if self.is_boss:
            print(f"🔥 [BOSS] {self.nama} melancarkan SERANGAN FATAL ke {target.nama} sebesar {self.attack} DMG!")
        else:
            print(f"👺 [Monster] {self.nama} menerkam {target.nama} sebesar {self.attack} DMG!")
            
        target.terima_damage(self.attack)

    def drop_loot(self, lantai):
        drop_chance = random.random()
        if not self.is_boss:
            # membuat loot drop kristal dengan peluang 10% dan tiap 20 lantai tingkat kristalnya naik 1
            if drop_chance < 0.1:
                kristal_level = 1 + (lantai // 20)
                print(f"💎 {self.nama} menjatuhkan Kristal Lv.{kristal_level}!")
                return int(kristal_level)
        else:
            # Boss selalu menjatuhkan kristal dengan level lebih tinggi dengan drop chance 50%
            if drop_chance < 0.5:
                kristal_level = 2 + (lantai // 20)
                print(f"🏆 [BOSS] {self.nama} menjatuhkan Kristal Lv.{kristal_level}!")
                return int(kristal_level)  

    def pesan_kematian(self):
        if self.is_boss:
            print(f"🏆 [BOSS] {self.nama} telah dikalahkan!")
        else:
            print(f"💀 [Monster] {self.nama} telah terbunuh!")

    