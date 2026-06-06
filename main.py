# ██████╗ ██╗ ██████╗██╗  ██╗    ███╗   ███╗███████╗    ██╗   ██╗██████╗ 
# ██╔══██╗██║██╔════╝██║ ██╔╝    ████╗ ████║██╔════╝    ██║   ██║██╔══██╗
# ██████╔╝██║██║     █████╔╝     ██╔████╔██║█████╗      ██║   ██║██████╔╝
# ██╔═══╝ ██║██║     ██╔═██╗     ██║╚██╔╝██║██╔══╝      ██║   ██║██╔═══╝ 
# ██║     ██║╚██████╗██║  ██╗    ██║ ╚═╝ ██║███████╗    ╚██████╔╝██║     
# ╚═╝     ╚═╝ ╚═════╝╚═╝  ╚═╝    ╚═╝     ╚═╝╚══════╝     ╚═════╝ ╚═╝


from function import *


if getattr(sys, 'frozen', False):
    ROOT_DIR = Path(sys.executable).parent
else:
    ROOT_DIR = Path(__file__).resolve().parent
sys.path.append(str(ROOT_DIR))



def main():
    antrean_gacha = Queue() # Antrian untuk menyimpan hero hasil gacha sebelum diklaim ke inventory
    navigasi = Stack() # Stack untuk menyimpan riwayat layar/menu yang dikunjungi
    
    # [AUTO-GENERATE] Periksa apakah file blueprint musuh & tower ada, jika tidak, buatkan dunia baru
    generate_world() # Fungsi untuk generate blueprint musuh & tower jika belum ada
        
    muat_hero() # Memuat data hero daari file json ke dlam game
    muat_musuh() # Memuat data musuh dari file json ke dalam game
    menara_game = siapkan_menara() # Siapkan struktur data menara dengan lantai dan musuhnya
    peta_game = siapkan_peta() # Siapkan Graph peta eksplorasi
    daftar_party = {"Party 1": []} # Dictionary untuk menyimpan formasi party, key = nama party, value = list ID hero
    id_dalam_antrean = set() # Set untuk melacak ID hero yang sudah ada di antrean gacha agar tidak duplikat
    inventory = {"tiket_gacha": 0} # Inventory untuk menyimpan item-item seperti tiket gacha, kristal, dll
    ekspedisi_aktif = {} # Dictionary untuk menyimpan data pengerahan ekspedisi {hero_id: data}
    # cek apakah ada save game yang bisa dimuat, kalau ada langsung load dan update state game
    cek_save_load(save_load.load_game(json_path / "savegame.json"), graveyard, daftar_party, barrack_aktif, menara_game, inventory, ekspedisi_aktif)
    navigasi.push("Lobi Utama") # Mulai di Lobi Utama
    
    while True:
        bersihkan_layar() # Membersihkan layar setiap kali masuk loop
        # Simpan progres setiap kali masuk loop untuk memastikan progress selalu tersimpan
        save_load_game(barrack_aktif, graveyard, daftar_party, menara_game, inventory, ekspedisi_aktif)
        layar_sekarang = navigasi.peek() # Update layar sekarang berdasarkan top stack navigasi
        
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
                save_load_game(barrack_aktif, graveyard, daftar_party, menara_game, inventory, ekspedisi_aktif)
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
            print("--- URUTKAN HERO ---")
            print("1. Berdasarkan ID")
            print("2. Berdasarkan Nama")
            print("3. Berdasarkan Level")
            print("4. Berdasarkan Bintang")
            print("0. KEMBALI ke Barrack")
            
            pilihan = input("> Pilih aksi: ")
            
            kumpulan_hero = list(barrack_aktif.values())
            
            if pilihan in ["1", "2", "3", "4"]:
                if pilihan == "1": kumpulan_hero = sort_heroes_by_id(kumpulan_hero)
                elif pilihan == "2": kumpulan_hero = sort_heroes_by_name(kumpulan_hero)
                elif pilihan == "3": kumpulan_hero = sort_heroes_by_level(kumpulan_hero)
                elif pilihan == "4": kumpulan_hero = sort_heroes_by_star(kumpulan_hero)
                
                print("\n--- DAFTAR HERO ---")
                for hero in kumpulan_hero:
                    print(f"ID: {hero.id}", end=" ")
                    hero.tampilkan_stats()
                input("\n(Tekan Enter untuk kembali)")
                
            elif pilihan == "0":
                navigasi.pop()

        # ==========================================
        # LOGIKA MENU: CARI HERO (Sub-menu Barrack)
        # ==========================================
        elif layar_sekarang == "Cari Hero":
            print("--- CARI HERO ---")
            print("1. Berdasarkan ID")
            print("2. Berdasarkan Nama")
            print("0. KEMBALI ke Barrack")
            
            pilihan = input("> Pilih aksi: ")
            
            if pilihan == "1":
                target_id = input("Masukkan ID Hero: ")
                kumpulan_hero = list(barrack_aktif.values())
                hasil = linear_search_hero_by_id(kumpulan_hero, target_id)
                if hasil:
                    print("\n[+] Hero Ditemukan:")
                    hasil.tampilkan_stats()
                else:
                    print("\n[-] Hero tidak ditemukan!")
                input("\n(Tekan Enter untuk lanjut)")
                
            elif pilihan == "2":
                target_name = input("Masukkan Nama Hero: ")
                kumpulan_hero = list(barrack_aktif.values())
                hasil = linear_search_hero_by_name(kumpulan_hero, target_name)
                if hasil:
                    print("\n[+] Hero Ditemukan:")
                    hasil.tampilkan_stats()
                else:
                    print("\n[-] Hero tidak ditemukan!")
                input("\n(Tekan Enter untuk lanjut)")
                
            elif pilihan == "0":
                navigasi.pop()
            else:
                input("Pilihan tidak valid! (Tekan Enter untuk lanjut)")

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
                            
                        if barrack_aktif[id_ditemukan].is_exploring:
                            print(f"[!] Gagal: {barrack_aktif[id_ditemukan].nama} sedang menjalani ekspedisi di luar!")
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
        # LOGIKA MENU: EKSPLORASI
        # ==========================================
        elif layar_sekarang == "Eksplorasi":
            print("--- SISTEM EKSPEDISI OTOMATIS (REAL-TIME) ---")
            print("1. Mulai Ekspedisi Baru")
            print("2. Cek Status Ekspedisi Aktif")
            print("0. KEMBALI ke Tower Gate")
            
            pilihan = input("> Pilih aksi: ")
            
            if pilihan == "1":
                if len(ekspedisi_aktif) >= 5:
                    print("\n[!] Batas maksimal ekspedisi tercapai! (Maks. 5 Ekspedisi)")
                    print("Tunggu hingga ada ekspedisi yang selesai terlebih dahulu.")
                    input("Tekan Enter untuk kembali...")
                    continue

                # CEK KETERSEDIAAN HERO
                hero_nganggur = []
                for h_id, h_obj in barrack_aktif.items():
                    dipakai_di_party = any(h_id in party for party in daftar_party.values())
                    if not dipakai_di_party and not h_obj.is_exploring:
                        hero_nganggur.append(h_obj)
                        
                if not hero_nganggur:
                    print("\n[!] Tidak ada hero yang tersedia untuk ekspedisi.")
                    print("Semua hero sedang berada di Party atau sedang dalam ekspedisi lain.")
                    input("Tekan Enter untuk kembali...")
                    continue
                    
                print("\n--- PILIH HERO UNTUK EKSPEDISI ---")
                for i, h in enumerate(hero_nganggur, 1):
                    print(f"{i}. {h.nama} [Lv.{h.level} | {h.star_level}⭐]")
                print("0. BATAL")
                
                pil_hero = input("> Pilih nomor hero: ")
                if pil_hero == "0":
                    continue
                if not (pil_hero.isdigit() and 1 <= int(pil_hero) <= len(hero_nganggur)):
                    input("\n[!] Pilihan tidak valid! (Tekan Enter)")
                    continue
                    
                hero_dipilih = hero_nganggur[int(pil_hero) - 1]
                
                # MULAI RANGKAI RUTE
                rute_ekspedisi = SingleLinkedList()
                lokasi_awal = "Desa Pemula"
                rute_ekspedisi.tambah_di_akhir(lokasi_awal, 0)
                lokasi_sementara = lokasi_awal
                total_waktu = 0
                
                print(f"\n[+] {hero_dipilih.nama} bersiap untuk berangkat!")
                print("[Membentuk Rute Ekspedisi]")
                while True:
                    print(f"\n📍 Posisi Saat Ini: {lokasi_sementara} | ⏱️ Total Waktu: {total_waktu} Detik")
                    jalan_tersedia = peta_game.lihat_jalan(lokasi_sementara)
                    
                    if not jalan_tersedia:
                        print("Jalan buntu! Rute ekspedisi berakhir di sini.")
                        break
                        
                    print("Pilih titik tujuan selanjutnya:")
                    for i, info in enumerate(jalan_tersedia, 1):
                        print(f"{i}. {info['tujuan']} (+{info['waktu']} Detik)")
                    print("0. SELESAI (Berangkatkan Ekspedisi)")
                    
                    pil_rute = input("> Pilih tujuan: ")
                    if pil_rute == "0":
                        break
                    elif pil_rute.isdigit() and 1 <= int(pil_rute) <= len(jalan_tersedia):
                        tujuan_dipilih = jalan_tersedia[int(pil_rute) - 1]
                        rute_ekspedisi.tambah_di_akhir(tujuan_dipilih['tujuan'], tujuan_dipilih['waktu'])
                        lokasi_sementara = tujuan_dipilih['tujuan']
                        total_waktu += tujuan_dipilih['waktu']
                    else:
                        print("[!] Pilihan tidak valid.")
                        
                # Menampilkan rute final
                daftar_rute = rute_ekspedisi.ambil_semua()
                if len(daftar_rute) > 1:
                    waktu_mulai = time.time()
                    waktu_selesai = waktu_mulai + total_waktu
                    
                    hero_dipilih.is_exploring = True
                    ekspedisi_aktif[hero_dipilih.id] = {
                        "nama_hero": hero_dipilih.nama,
                        "waktu_mulai": waktu_mulai,
                        "waktu_selesai": waktu_selesai,
                        "waktu_total": total_waktu,
                        "rute": [item["tujuan"] for item in daftar_rute]
                    }
                    
                    print("\n" + "="*40)
                    print("🚀 EKSPEDISI DIBERANGKATKAN! 🚀")
                    print(f"Hero Ditugaskan : {hero_dipilih.nama}")
                    print(f"Total Waktu     : {total_waktu} Detik")
                    print("Rute Perjalanan :")
                    print(" ➔ ".join(ekspedisi_aktif[hero_dipilih.id]["rute"]))
                    print("="*40)
                    print("Ekspedisi berjalan secara real-time di belakang layar.")
                else:
                    print(f"\n[-] Ekspedisi dibatalkan ({hero_dipilih.nama} tetap di Desa Pemula).")
                    
                input("\nTekan Enter untuk kembali...")
                
            elif pilihan == "2":
                print("\n--- STATUS EKSPEDISI AKTIF ---")
                if not ekspedisi_aktif:
                    print("Tidak ada ekspedisi yang sedang berjalan.")
                else:
                    waktu_sekarang = time.time()
                    selesai_list = []
                    
                    for h_id, data in ekspedisi_aktif.items():
                        sisa_waktu = int(data["waktu_selesai"] - waktu_sekarang)
                        
                        if sisa_waktu <= 0:
                            # Ekspedisi Selesai
                            selesai_list.append(h_id)
                            print(f"[✅ SELESAI] {data['nama_hero']} telah kembali dari {data['rute'][-1]}.")
                        else:
                            print(f"[🏃 BERJALAN] {data['nama_hero']} - Sisa Waktu: {sisa_waktu} detik.")
                    
                    # Bersihkan ekspedisi yang selesai
                    for h_id in selesai_list:
                        if h_id in barrack_aktif:
                            barrack_aktif[h_id].is_exploring = False
                        del ekspedisi_aktif[h_id]
                        
                input("\nTekan Enter untuk kembali...")
                
            elif pilihan == "0":
                navigasi.pop()
            else:
                input("\n[!] Pilihan tidak valid! (Tekan Enter)")

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