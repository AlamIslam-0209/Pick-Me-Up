# ██████╗ ██╗ ██████╗██╗  ██╗    ███╗   ███╗███████╗    ██╗   ██╗██████╗ 
# ██╔══██╗██║██╔════╝██║ ██╔╝    ████╗ ████║██╔════╝    ██║   ██║██╔══██╗
# ██████╔╝██║██║     █████╔╝     ██╔████╔██║█████╗      ██║   ██║██████╔╝
# ██╔═══╝ ██║██║     ██╔═██╗     ██║╚██╔╝██║██╔══╝      ██║   ██║██╔═══╝ 
# ██║     ██║╚██████╗██║  ██╗    ██║ ╚═╝ ██║███████╗    ╚██████╔╝██║     
# ╚═╝     ╚═╝ ╚═════╝╚═╝  ╚═╝    ╚═╝     ╚═╝╚══════╝     ╚═════╝ ╚═╝
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
sys.path.append(str(ROOT_DIR))

from function import *
from Algoritma.recursion import hitung_kebutuhan_kristal
from StrukturData.Stack import Stack
from StrukturData.Queue import Queue 

def main():
    antrean_gacha = Queue()
    navigasi = Stack()
    muat_hero()
    muat_musuh()
    menara_game = siapkan_menara()
    daftar_party = {"Party 1": []}
    id_dalam_antrean = set()
    inventory = {"tiket_gacha": 0}
    cek_save_load(save_load.load_game(json_path / "savegame.json"), graveyard, daftar_party, barrack_aktif, menara_game, inventory)
    navigasi.push("Lobi Utama")
    
    while True:
        bersihkan_layar()
        
        layar_sekarang = navigasi.peek()
        
        print("="*45)
        print(f"POSISI SEKARANG: {layar_sekarang.upper()}")
        print("="*45)
        
        # ==========================================
        # LOGIKA MENU: LOBI UTAMA
        # ==========================================
        if layar_sekarang == "Lobi Utama":
            print("1. Pergi ke Summon Hall (Gacha)")
            print("2. Pergi ke Barrack (Atur Party)")
            print("3. Pergi ke Tower Gate ")
            print("0. Keluar dari Game")
            
            pilihan = input("> Pilih aksi (0-3): ")
            
            if pilihan == "1":
                navigasi.push("Summon Hall")  
            elif pilihan == "2":
                navigasi.push("Barrack")
            elif pilihan == "3":
                navigasi.push("Tower Gate")
            elif pilihan == "0":
                print("Menyimpan progres... Sampai jumpa, Master!")
                # Siapkan data save
                save_data = {}
                save_data["barrack_aktif"] = {}
                for h_id, hero_obj in barrack_aktif.items():
                    save_data["barrack_aktif"][h_id] = {
                        "id": hero_obj.id,
                        "name": hero_obj.nama,
                        "hp": hero_obj.hp,
                        "hp_max": hero_obj.hp_max,
                        "attack": hero_obj.attack,
                        "level": hero_obj.level,
                        "star_level": hero_obj.star_level,
                        "equipment": {"weapon": getattr(hero_obj, "weapon", None)},
                        "is_alive": hero_obj.is_alive,
                        "exp": getattr(hero_obj, "exp", 0),
                        "exp_next": getattr(hero_obj, "exp_next", hero_obj.level*100)
                    }
                save_data["graveyard"] = list(graveyard)
                save_data["daftar_party"] = daftar_party
                save_data["menara"] = {"current_floor": menara_game.lantai_sekarang.data.get("no_lantai")}
                save_data["inventory"] = inventory
                save_load.save_game(json_path / "savegame.json", save_data)
                break 
            else:
                input("Pilihan tidak valid! (Tekan Enter untuk lanjut)")

        # ==========================================
        # LOGIKA MENU: BARRACK
        # ==========================================
        elif layar_sekarang == "Barrack":
            print("1. Lihat Daftar Hero (Sorting)")
            print("2. Cari Hero Spesifik (Searching)")
            print("3. Atur Party")
            print("4. Ruang Evolusi")
            print("0. KEMBALI ke Lobi Utama")
            
            pilihan = input("> Pilih aksi (0-4): ")
            
            if pilihan == "1":
                navigasi.push("Daftar Hero") 
            elif pilihan == "2":
                navigasi.push("Cari Hero")
            elif pilihan == "3":
                navigasi.push("Party")
            elif pilihan == "4":
                navigasi.push("Ruang Evolusi")
            elif pilihan == "0":
                navigasi.pop() 

        # ==========================================
        # LOGIKA MENU: DAFTAR HERO (Sub-menu Barrack)
        # ==========================================
        elif layar_sekarang == "Daftar Hero":
            kumpulan_hero = list(barrack_aktif.values()) 
            for hero in kumpulan_hero:
                hero.tampilkan_stats()
            print("\n0. KEMBALI ke Barrack")
            
            pilihan = input("> Pilih aksi: ")
            
                
            if pilihan == "0":
                navigasi.pop()
                

        # ==========================================
        # LOGIKA MENU: ATUR PARTY
        # ==========================================
        elif layar_sekarang == "Party":
            
            hero_terpakai = set()
            for anggota in daftar_party.values():
                for h_id in anggota:
                    hero_terpakai.add(h_id)

            print("--- DAFTAR HERO TERSEDIA ---")
            if not barrack_aktif:
                print("[Kosong] Kamu belum punya hero. Gacha dulu sana!")
            else:
                ada_hero_nganggur = False
                for h_id, hero in barrack_aktif.items():
                    if h_id not in hero_terpakai:
                        print(f"ID: {h_id} | {hero.nama} ({hero.star_level}⭐): Lv.{hero.level}")
                        ada_hero_nganggur = True
                
                if not ada_hero_nganggur:
                    print("- Semua heromu sudah ditugaskan ke medan tempur! -")
            
            print("\n--- SLOT PARTY ---")
            for nama_party, anggota in daftar_party.items():
                status = f"{len(anggota)}/5 Hero" if anggota else "KOSONG"
                print(f"- {nama_party} : [{status}]")
                
            print("\n1. Edit Party") 
            print("9. Tambah Slot Party Baru") 
            print("0. KEMBALI ke Barrack")
            
            pilihan = input("> Pilih aksi: ")
            
            if pilihan == "1":
                target_party = input("\nMasukkan nama party yang ingin diedit (Cth: Party 1): ")
                lst_nama = []
                
                if target_party not in daftar_party:
                    print(f"[!] Gagal: {target_party} tidak ditemukan!")
                    input("Tekan Enter untuk kembali...")
                else:
                    print(f"\n[MENGEDIT {target_party.upper()}]")                    
                    print("(Hero yang sedang dipakai di party ini bisa dimasukkan kembali)")
                    
                    for i in range(1, 6):
                        if i == 1:
                            lst_nama.append(input("Masukkan NAMA KAPTEN (Kosongkan jika tidak ada): ").strip())
                        else:
                            lst_nama.append(input(f"Masukkan NAMA ANGGOTA {i-1} (Kosongkan jika tidak ada): ").strip())
                    
                    if lst_nama[0] == "" and any(nama != "" for nama in lst_nama[1:]):
                        print("\n[!] Gagal: Posisi KAPTEN wajib diisi terlebih dahulu sebelum anggota lain!")
                        input("Tekan Enter untuk lanjut...")
                        continue
                        
                    nama_dimasukkan = [nama for nama in lst_nama if nama != ""]
                    
                    id_dimasukkan = []
                    valid = True
                    
                    for nama_target in nama_dimasukkan:
                        id_ditemukan = None
                        
                        for h_id, hero_obj in barrack_aktif.items():
                            if hero_obj.nama.lower() == nama_target.lower():
                                id_ditemukan = h_id
                                break
                        
                        if id_ditemukan is None:
                            print(f"[!] Gagal: Hero dengan nama '{nama_target}' tidak ada di Barrack!")
                            valid = False
                            break
                            
                        if id_ditemukan in id_dimasukkan:
                            print(f"[!] Gagal: {barrack_aktif[id_ditemukan].nama} sudah terdaftar di party ini!")
                            valid = False
                            break
                            
                        for nama_p, anggota_p in daftar_party.items():
                            if nama_p != target_party and id_ditemukan in anggota_p:
                                print(f"[!] Gagal: {barrack_aktif[id_ditemukan].nama} sedang bertugas di {nama_p}!")
                                valid = False
                                break
                                
                        if not valid:
                            break
                            
                        id_dimasukkan.append(id_ditemukan)
                    
                    if not valid:
                        input("Tekan Enter untuk lanjut...")
                        
                    if valid:
                        daftar_party[target_party] = id_dimasukkan
                        print(f"[+] {target_party} berhasil disimpan dengan {len(id_dimasukkan)} Hero!")
                        input("Tekan Enter untuk lanjut...")

            elif pilihan == "9":
                nomor_baru = len(daftar_party) + 1
                nama_baru = f"Party {nomor_baru}"
                
                daftar_party[nama_baru] = []
                print(f"\n[+] {nama_baru} berhasil dibuat! Gunakan menu Edit untuk mengisi hero.")
                input("Tekan Enter untuk lanjut...")
                    
            elif pilihan == "0":
                navigasi.pop()
        # ==========================================
        # LOGIKA MENU: RUANG EVOLUSI
        # ==========================================
        elif layar_sekarang == "Ruang Evolusi":
            tampilkan_kristal(inventory)
            print("\n1. Evolusi Hero")
            print("2. Sintesis Kristal (Pabrik)")
            print("0. KEMBALI ke Barrack")
            
            pilihan = input("> Pilih aksi: ")
            
            if pilihan == "1":
                print("\n--- DAFTAR HERO SIAP EVOLUSI ---")
                bisa_evolusi = []
                for h_id, hero in barrack_aktif.items():
                    if hero.level >= hero.max_level and hero.star_level < 7:
                        bisa_evolusi.append(hero)
                        print(f"[{hero.id}] {hero.nama} ({hero.star_level}⭐) - Lv.{hero.level}")
                
                if not bisa_evolusi:
                    input("\nTidak ada hero yang siap dievolusi (Harus Max Level & < 7⭐). Tekan Enter...")
                else:
                    target_id = input("\nMasukkan ID Hero yang ingin dievolusi (0 Batal): ").upper()
                    if target_id != "0":
                        target_hero = next((h for h in bisa_evolusi if h.id == target_id), None)
                        
                        if target_hero:
                            # Butuh kristal level = star_level + 1
                            kristal_dibutuhkan = target_hero.star_level + 1
                            if inventory["kristal"].get(kristal_dibutuhkan, 0) >= 1:
                                inventory["kristal"][kristal_dibutuhkan] -= 1
                                target_hero.evolusi()
                                input("Tekan Enter untuk lanjut...")
                            else:
                                print(f"\n[!] Gagal: Membutuhkan 1 Kristal {NAMA_KRISTAL[kristal_dibutuhkan]} (Lv.{kristal_dibutuhkan})!")
                                input("Tekan Enter untuk lanjut...")
                        else:
                            input("\n[!] ID tidak valid. Tekan Enter...")
                            
            elif pilihan == "2":
                print("\n--- SINTESIS KRISTAL ---")
                print("Setiap kristal butuh 5 kristal 1 tingkat di bawahnya.")
                print("Gunakan Kalkulator Rekursi untuk menghitung total ekuivalen Kristal Merah!")
                print("\n1. Sintesis Kristal Manual (Naik 1 Tingkat)")
                print("2. Kalkulator Kebutuhan (Rekursi)")
                sub_pil = input("> Pilih: ")
                
                if sub_pil == "1":
                    try:
                        tgt_lvl = int(input("Masukkan level kristal target (2-7): "))
                        if 2 <= tgt_lvl <= 7:
                            jml = int(input("Jumlah yang ingin disintesis: "))
                            if jml > 0:
                                butuh = jml * 5
                                sisa = inventory["kristal"].get(tgt_lvl - 1, 0)
                                if sisa >= butuh:
                                    inventory["kristal"][tgt_lvl - 1] -= butuh
                                    inventory["kristal"][tgt_lvl] = inventory["kristal"].get(tgt_lvl, 0) + jml
                                    print(f"\n[+] Berhasil mensintesis {jml} Kristal {NAMA_KRISTAL[tgt_lvl]}!")
                                else:
                                    print(f"\n[!] Gagal: Butuh {butuh} Kristal {NAMA_KRISTAL[tgt_lvl-1]} (Hanya punya {sisa}).")
                            else:
                                print("\nJumlah tidak valid.")
                        else:
                            print("\nLevel target harus 2 hingga 7.")
                    except ValueError:
                        print("\nMasukan harus berupa angka.")
                    input("Tekan Enter untuk lanjut...")
                    
                elif sub_pil == "2":
                    try:
                        tgt_lvl = int(input("Ingin membuat kristal level berapa? (2-7): "))
                        if 2 <= tgt_lvl <= 7:
                            jml = int(input("Jumlah yang ingin dibuat: "))
                            if jml > 0:
                                total_merah = hitung_kebutuhan_kristal(1, tgt_lvl, jml)
                                print(f"\n[INFO] Berdasarkan perhitungan REKURSI:")
                                print(f"Untuk membuat {jml} Kristal {NAMA_KRISTAL[tgt_lvl]} (Lv.{tgt_lvl}),")
                                print(f"Kamu setara membutuhkan total {total_merah} Kristal Merah (Lv.1)!")
                            else:
                                print("\nJumlah tidak valid.")
                        else:
                            print("\nLevel harus 2 hingga 7.")
                    except ValueError:
                        print("\nMasukan harus berupa angka.")
                    input("Tekan Enter untuk lanjut...")
                    
            elif pilihan == "0":
                navigasi.pop()

        # ==========================================
        # LOGIKA MENU: SUMMON HALL
        # ==========================================
        elif layar_sekarang == "Summon Hall":
            print(f"--- ANTREAN KLAIM: {antrean_gacha.size()} Hero Menunggu ---")
            print(f"--- TIKET GACHA: {inventory.get('tiket_gacha', 0)}x Tiket (1 Tiket = 10 Pull) ---")
            print("-" * 45)
            
            print("1. Tarik 10x Hero Baru (Gacha)")
            print("2. Klaim 1 Hero dari Antrean")
            print("0. KEMBALI ke Lobi Utama")
            
            pilihan = input("> Pilih aksi: ")
            
            if pilihan == "1":
                if inventory.get("tiket_gacha", 0) > 0:
                    print("\n[+] Menarik 10 Hero ke dalam antrean...")
                    inventory["tiket_gacha"] -= 1
                    for i in range(10):
                        hero_gacha = proses_gacha(id_dalam_antrean)
                        
                        if hero_gacha:
                            antrean_gacha.enqueue(hero_gacha)
                            id_dalam_antrean.add(hero_gacha.id) 
                    
                    input("Gacha selesai! 10 Hero telah masuk antrean. Sisa Tiket: " + str(inventory["tiket_gacha"]) + " (Tekan Enter)")
                else:
                    input("\n[!] Gagal: Kamu tidak punya Tiket Gacha. Kalahkan boss lantai untuk mendapatkannya! (Tekan Enter)")
                
            elif pilihan == "2":
                if antrean_gacha.is_empty():
                    input("\n[!] Antrean kosong! Kamu harus Gacha dulu. (Tekan Enter)")
                else:
                    hero_diklaim = antrean_gacha.dequeue()
                    id_dalam_antrean.remove(hero_diklaim.id)
                    barrack_aktif[hero_diklaim.id] = hero_diklaim 
                    
                    print(f"[+] Berhasil memanggil: {hero_diklaim.nama} ({hero_diklaim.star_level}⭐)")
                    input("Hero telah dimasukkan ke Inventory. (Tekan Enter)")
                    
            elif pilihan == "0":
                navigasi.pop()
                
                
        # ==========================================
        # LOGIKA MENU: TOWER GATE
        # ==========================================
        elif layar_sekarang == "Tower Gate":
            print("1. Panjat Tower")
            print("2. Eksplorasi")
            print("0. KEMBALI ke Lobi Utama")
            
            pilihan = input("> Pilih aksi (0-3): ")
            
            if pilihan == "1":
                navigasi.push("Tower")  # Pindah menu = Push
            elif pilihan == "2":
                navigasi.push("Eksplorasi")
            elif pilihan == "0":
                navigasi.pop()
            else:
                input("Pilihan tidak valid! (Tekan Enter untuk lanjut)")
                
                
        # ==========================================
        # LOGIKA MENU: TOWER (PILIH LANTAI)
        # ==========================================
        elif layar_sekarang == "Tower":
            print("--- MENU PANJAT TOWER ---")
            
            lantai_tersedia = []
            current_node = menara_game.head
            
            while current_node is not None:
                data_l = current_node.data
                
                is_puncak = (current_node == menara_game.lantai_sekarang)
                if is_puncak or not data_l['is_boss']:
                    lantai_tersedia.append(current_node)
                
                if is_puncak:
                    break
                    
                current_node = current_node.next
                
            print("Pilih lantai untuk pertempuran:")
            for idx, node_lantai in enumerate(lantai_tersedia):
                data = node_lantai.data
                status = "[PUNCAK SAAT INI]" if node_lantai == menara_game.lantai_sekarang else "[FARMING]"
                print(f"{idx + 1}. Lantai {data['no_lantai']} - {data['nama_lokasi']} {status}")
                
            print("0. KEMBALI ke Tower Gate")
            
            pilihan = input(f"> Pilih lantai (0 - {len(lantai_tersedia)}): ")
            
            if pilihan == "0":
                navigasi.pop()
                
            elif pilihan.isdigit() and 1 <= int(pilihan) <= len(lantai_tersedia):
                lantai_pilihan = lantai_tersedia[int(pilihan) - 1]
                data_pilihan = lantai_pilihan.data
                
                print(f"\n[+] Memasuki Lantai {data_pilihan['no_lantai']} ({data_pilihan['nama_lokasi']})...")
                
                party_aktif = {k: v for k, v in daftar_party.items() if len(v) > 0}
                
                if not party_aktif:
                    print("[!] Kamu belum memiliki Party yang terisi! Atur formasi di menu Barrack terlebih dahulu.")
                    input("Tekan Enter untuk kembali...")
                    continue 
                
                list_nama_party = list(party_aktif.keys())
                
                print("\n--- DAFTAR PARTY SIAP TEMPUR ---")
                for i, nama_p in enumerate(list_nama_party, 1):
                    nama_hero = [barrack_aktif[h_id].nama for h_id in party_aktif[nama_p]]
                    print(f"{i}. {nama_p} -> [{', '.join(nama_hero)}]")
                
                master_entity = Entity("Master Whatevr", hp=999, attack=999, level=999)
                master_node = RaidNode(master_entity, "Master")
                
                party_terpilih = []
                
                is_boss = data_pilihan['is_boss']
                
                if not is_boss:
                    print("\n[Lantai Biasa] Kamu hanya diizinkan membawa 1 Party.")
                    pilih_idx = input(f"> Pilih Party (1-{len(list_nama_party)}): ")
                    
                    if pilih_idx.isdigit() and 1 <= int(pilih_idx) <= len(list_nama_party):
                        party_terpilih.append(list_nama_party[int(pilih_idx) - 1])
                    else:
                        print("[!] Pilihan tidak valid.")
                        input("Tekan Enter untuk membatalkan...")
                        continue
                else:
                    print("\n[LANTAI BOSS] Kamu bisa membawa hingga 2 Party!")
                    pilih_1 = input(f"> Pilih Party PERTAMA (1-{len(list_nama_party)}): ")
                    
                    if pilih_1.isdigit() and 1 <= int(pilih_1) <= len(list_nama_party):
                        party_terpilih.append(list_nama_party[int(pilih_1) - 1])
                    else:
                        print("[!] Pilihan tidak valid.")
                        input("Tekan Enter untuk membatalkan...")
                        continue
                        
                    if len(list_nama_party) > 1:
                        pilih_2 = input(f"> Pilih Party KEDUA (Ketik 0 jika hanya ingin bawa 1 party): ")
                        if pilih_2.isdigit() and 1 <= int(pilih_2) <= len(list_nama_party) and pilih_2 != "0":
                            if pilih_2 == pilih_1:
                                print("[!] Party tidak boleh sama! Membawa 1 party saja.")
                            else:
                                party_terpilih.append(list_nama_party[int(pilih_2) - 1])

                for nama_p in party_terpilih:
                    id_anggota = party_aktif[nama_p]
                    
                    kapten_obj = barrack_aktif[id_anggota[0]]
                    kapten_node = RaidNode(kapten_obj, "Kapten")
                    
                    for h_id in id_anggota[1:]:
                        anggota_obj = barrack_aktif[h_id]
                        anggota_node = RaidNode(anggota_obj, "Anggota")
                        kapten_node.tambah_unit(anggota_node) 
                        
                    master_node.tambah_unit(kapten_node)

                print("\n[Formasi Terbentuk]")
                master_node.tampilkan_struktur_raid()
                
                master_musuh_entity = Entity("Pasukan Musuh", hp=999, attack=999)
                master_musuh_node = RaidNode(master_musuh_entity, "Master Musuh")
                
                for m_id in data_pilihan['id_musuh']:
                    cek_boss = "BOSS" in m_id 
                    
                    if m_id in Daftar_Musuh:
                        blueprint = Daftar_Musuh[m_id]
                        m_nama = blueprint["name"]
                        m_hp = blueprint["hp"]
                        m_atk = blueprint["atk"]
                    else:
                        m_nama = m_id
                        m_hp = 500 if cek_boss else random.randint(20, 50)
                        m_atk = 150 if cek_boss else random.randint(15, 30)
                    
                    m_entity = Enemy(nama=m_nama, hp=m_hp, atk=m_atk, is_boss=cek_boss)
                    m_node = RaidNode(m_entity, "Monster")
                    
                    master_musuh_node.tambah_unit(m_node)
                
                arena_cll = CircularLinkedList()
                
                menang = jalankan_raid_kombat(master_node, master_musuh_node, arena_cll)
                
                print("\n--- MENGEVALUASI KONDISI PASUKAN ---")
                cek_kematian(daftar_party)
                cek_status(master_node)
                
                if menang:
                    data_pilihan['is_cleared'] = True
                    
                    print("\nLANTAI SELESAI! Memberikan Reward & Pemulihan...")
                    
                    hadiah_xp = data_pilihan['no_lantai'] * 15
                    if is_boss: hadiah_xp *= 10
                    print("Semua hero mendapatkan", hadiah_xp, "EXP")
                    is_first_clear = (lantai_pilihan == menara_game.lantai_sekarang and not inventory.get("tamat", False))
                    
                    if is_boss and is_first_clear:
                        inventory["tiket_gacha"] = inventory.get("tiket_gacha", 0) + 1
                        print("🎉 BONUS BOSS: Mendapatkan 1x Tiket Gacha (10 Pulls)!")
                    
                    for nama_p in party_terpilih:
                        for h_id in daftar_party[nama_p]:
                            hero_obj = barrack_aktif[h_id]
                            
                            hero_obj.tambah_xp(hadiah_xp)
                            hero_obj.pulihkan_kondisi()
                    
                    print("═"*45 + "\n")
                    if lantai_pilihan == menara_game.lantai_sekarang:
                        if menara_game.NaikLantai():
                            print(f"\n[+] PROGRESS: Bergerak maju ke Lantai {menara_game.lantai_sekarang.data['no_lantai']}")
                        else:
                            inventory["tamat"] = True
                            print(f"\n[+] TOWER CLEARED! Kamu sudah mencapai puncak menara!")
                    else:
                        print(f"\n[+] berhasil menyelesaikan lantai {data_pilihan["no_lantai"]}")
                        
                            
                input("\nTekan Enter untuk kembali ke menu Tower...")
                
            else:
                input("\n[!] Pilihan tidak valid! (Tekan Enter)")



if __name__ == "__main__":
    main()