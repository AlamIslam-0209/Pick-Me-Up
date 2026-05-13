import Node as n

class CircularLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.giliran_sekarang = None
        
    def TambahEntity(self, entity):
        giliran_berikutnya = n.Node(entity)
        if not self.head:
            self.head = giliran_berikutnya
            self.tail = giliran_berikutnya
            self.head.next = self.head
        else: #klo udah ada isinya
            self.tail.next = giliran_berikutnya
            self.tail = giliran_berikutnya
            self.tail.next = self.head    
        
    def Mulai(self):
        self.giliran_sekarang = self.head
        return self.giliran_sekarang
        
    def NextTurn(self):
        if self.giliran_sekarang:
            self.giliran_sekarang = self.giliran_sekarang.next
            return self.giliran_sekarang
        return None
    
def siapkan_pasukan_ke_arena(node_tree, arena_cll):
    """Menelusuri Tree dan memasukkan tiap karakter ke antrean bertarung (CLL)"""
    
    arena_cll.TambahEntity(node_tree)
    
    for bawahan in node_tree.anak:
        siapkan_pasukan_ke_arena(bawahan, arena_cll)
        
        
def jalankan_raid_kombat(master_tree, boss_node, arena_cll):
    arena_cll.TambahEntity(boss_node)
    
    # 2. Masukkan seluruh formasi Tree ke arena pakai fungsi rekursif tadi
    siapkan_pasukan_ke_arena(master_tree, arena_cll)
    
    print("\n⚔️ RAID BOSS DIMULAI! ⚔️")
    
    # 3. Mulai muter gilirannya!
    giliran_aktif = arena_cll.Mulai()
    
    # Contoh 3 Turn (Putaran) pertempuran
    for turn in range(1, 4):
        petarung = giliran_aktif.data
        
        # Mengecek apakah ini Boss atau Pasukan kita
        if petarung.nama == "BOSS NAGA":
            print(f"[{turn}] 🐉 BOSS NAGA mengaum siap menyerang!")
            # Logika boss nyerang random atau nyerang satu cabang (Party)
            
        else:
            # Mengecek jabatan lewat Tree
            if petarung.peran == "Kapten":
                print(f"[{turn}] 🗡️ {petarung.nama} (KAPTEN) memberikan aba-aba serangan!")
                # Kasih buff ke anggota di bawahnya (petarung.anak)
            elif petarung.peran == "Anggota":
                print(f"[{turn}] 🏹 {petarung.nama} menyerang boss!")
                
        # Lanjut ke orang berikutnya di CLL
        giliran_aktif = arena_cll.NextTurn()
    
# if __name__ == "__main__":
#     class DummyKarakter:
#         def __init__(self, nama, tipe):
#             self.nama = nama
#             self.tipe = tipe

#     arena = CircularLinkedList()
    
#     arena.TambahEntity(DummyKarakter("Han", "Hero"))
#     arena.TambahEntity(DummyKarakter("Jenna", "Hero"))
#     arena.TambahEntity(DummyKarakter("BOSS_01", "Monster"))
    
#     print("--- BATTLE START ---")
#     giliran = arena.Mulai()
#     print(f"Giliran 1: {giliran.data.nama} ({giliran.data.tipe})")
    
#     giliran = arena.NextTurn()
#     print(f"Giliran 2: {giliran.data.nama} ({giliran.data.tipe})")
    
#     giliran = arena.NextTurn()
#     print(f"Giliran 3: {giliran.data.nama} ({giliran.data.tipe})")
    
#     giliran = arena.NextTurn()
#     print(f"Giliran 4: {giliran.data.nama} ({giliran.data.tipe}) ")

