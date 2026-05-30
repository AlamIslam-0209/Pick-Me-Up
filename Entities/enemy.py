from Entities.entity import Entity

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