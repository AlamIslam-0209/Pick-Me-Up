from .entity import Entity

class Hero(Entity):
    def __init__(self, data_dict):
        super().__init__(
            nama = data_dict['name'],
            hp = data_dict['hp'],
            attack = data_dict['attack'],
            level = data_dict.get('level', 1)
        )
        self.id = data_dict['id'] # Sangat penting untuk fitur Permadeath
        self.star_level = data_dict['star_level']
        self.weapon = data_dict['equipment']['weapon']

    def tampilkan_stats(self):
        status = "Hidup" if self.is_alive else "GUGUR"
        print(f"[{self.star_level}⭐] {self.nama} (Lv.{self.level}) - {status}")
        print(f"    Senjata: {self.weapon} | HP: {self.hp}/{self.hp_max} | ATK: {self.attack}")