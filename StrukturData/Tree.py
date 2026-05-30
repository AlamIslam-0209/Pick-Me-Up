class RaidNode:
    def __init__(self, objek_entitas, peran):
        self.entitas = objek_entitas 
        self.peran = peran           # "Master", "Kapten", "Anggota", "Monster"
        self.anak = []      
        
    def tambah_unit(self, node_baru):
        """
        Menambahkan anggota baru ke dalam formasi. Posisi Kapten dibatasi maksimal 4 anggota.
        """
        if self.peran == "Kapten" and len(self.anak) >= 4:
            print(f"[!] Gagal: Party Kapten {self.entitas.nama} sudah penuh.")
            return False
        
        self.anak.append(node_baru)
        return True

    def tampilkan_struktur_raid(self, level=0):
        """
        Menampilkan struktur hierarki anggota party ke layar secara berjenjang.
        """
        indentasi = "    " * level
        
        print(f"{indentasi} {self.entitas.nama} ({self.peran}) - HP: {self.entitas.hp}")
        
        for unit in self.anak:
            unit.tampilkan_struktur_raid(level + 1)