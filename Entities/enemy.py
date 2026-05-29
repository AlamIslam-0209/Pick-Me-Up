from Entities.entity import Entity

class Enemy(Entity):
    def __init__(self, nama, hp, atk, is_boss=False):
        # super() memanggil __init__ dari class Entity
        # parameter 'atk' dari main.py dihubungkan ke 'attack' milik Entity
        super().__init__(nama=nama, hp=hp, attack=atk)
        
        # Atribut khusus Enemy
        self.is_boss = is_boss

    # Konsep Polymorphism: Menimpa method serang() dari parent class
    # agar tampilannya berbeda saat musuhnya adalah BOSS
    def serang(self, target):
        if self.is_boss:
            print(f"🔥 [BOSS] {self.nama} melancarkan SERANGAN FATAL ke {target.nama} sebesar {self.attack} DMG!")
        else:
            print(f"👺 [Monster] {self.nama} menerkam {target.nama} sebesar {self.attack} DMG!")
            
        target.terima_damage(self.attack)