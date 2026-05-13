import StrukturData.Tower.Node as n
import time
import random # Tambahan untuk logika musuh memilih target acak

class CircularLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.giliran_sekarang = None
        
    def TambahEntity(self, node_tree):
        giliran_berikutnya = n.Node(node_tree)
        if not self.head:
            self.head = giliran_berikutnya
            self.tail = giliran_berikutnya
            self.head.next = self.head
        else: 
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
    
def siapkan_pasukan_ke_arena(node_tree, arena_cll, daftar_pasukan):
    """Menelusuri Tree dan HANYA memasukkan Kapten & Anggota ke arena"""
    
    # Master tidak diizinkan masuk ke arena pertarungan
    if node_tree.peran in ["Kapten", "Anggota"] and node_tree.entitas.is_alive:
        arena_cll.TambahEntity(node_tree)
        daftar_pasukan.append(node_tree) # Simpan ke list untuk jadi target monster
    
    for bawahan in node_tree.anak:
        siapkan_pasukan_ke_arena(bawahan, arena_cll, daftar_pasukan)
        
        
def jalankan_raid_kombat(master_tree, boss_node, arena_cll):
    # 1. Masukkan Boss ke arena
    arena_cll.TambahEntity(boss_node)
    
    # 2. Masukkan formasi Tree (Kecuali Master) ke arena
    pasukan_hero = []
    siapkan_pasukan_ke_arena(master_tree, arena_cll, pasukan_hero)
    
    print("\n" + "="*45)
    print(f"⚔️ RAID BOSS DIMULAI: Menghadapi {boss_node.entitas.nama}! ⚔️")
    print("="*45)
    
    giliran_aktif = arena_cll.Mulai()
    turn = 1
    
    # 3. Game Loop Pertarungan (Berputar sampai Boss mati atau SEMUA HERO mati)
    while boss_node.entitas.is_alive:
        # Cek apakah masih ada hero yang hidup untuk ditarget
        hero_hidup = [h for h in pasukan_hero if h.entitas.is_alive]
        
        # Kalau semua hero sudah mati, pertarungan berakhir (Kalah)
        if not hero_hidup:
            break
            
        # Ekstrak data dari Node
        node_petarung = giliran_aktif.data
        entitas_aktif = node_petarung.entitas
        
        # Jika petarung mati karena efek racun atau serangan sebelumnya, skip giliran
        if not entitas_aktif.is_alive:
            giliran_aktif = arena_cll.NextTurn()
            continue
            
        print(f"\n[Turn {turn}] ⏳ Giliran: {entitas_aktif.nama} (HP: {entitas_aktif.hp}/{entitas_aktif.hp_max})")
        time.sleep(1) 
        
        # LOGIKA SERANG
        if node_petarung.peran == "Monster":
            # Monster menyerang salah satu hero yang MASIH HIDUP secara acak
            target_hero = random.choice(hero_hidup)
            entitas_aktif.serang(target_hero.entitas)
        else:
            # Pahlawan menyerang Boss
            entitas_aktif.serang(boss_node.entitas)
            
        turn += 1
        giliran_aktif = arena_cll.NextTurn()
    
    # HASIL PERTEMPURAN
    print("\n" + "="*45)
    if not boss_node.entitas.is_alive:
        print("🎉 VICTORIOUS! Boss telah dihancurkan. Lantai diselesaikan!")
        return True # Lantai bisa di-clear
    else:
        print("💀 DEFEAT! Seluruh party hancur, Master terpaksa mundur dari pertempuran...")
        return False