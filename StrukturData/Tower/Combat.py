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

