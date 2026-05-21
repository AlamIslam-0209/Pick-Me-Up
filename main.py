import sys
import os
import random
import time
from pathlib import Path
import customtkinter as ctk
from tkinter import messagebox

ROOT_DIR = Path(__file__).resolve().parent
sys.path.append(str(ROOT_DIR))

from function import *
from Algoritma.recursion import hitung_kebutuhan_kristal
from StrukturData.Queue import Queue

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class PickMeUpGame(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Pick Me Up - GUI Edition")
        self.geometry("1000x700")
        
        # Game State
        self.inventory = {"tiket_gacha": 0, "kristal": {i: 0 for i in range(1, 8)}}
        self.daftar_party = {"Party 1": []}
        self.antrean_gacha = Queue()
        
        # Load Data
        muat_hero()
        muat_musuh()
        self.menara_game = siapkan_menara()
        
        # Load Save
        cek_save_load(save_load.load_game(json_path / "savegame.json"), 
                      graveyard, self.daftar_party, barrack_aktif, 
                      self.menara_game, self.inventory)
        
        # UI Container
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.show_main_lobby()
        
    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()
            
    def save_and_quit(self):
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
        save_data["daftar_party"] = self.daftar_party
        save_data["menara"] = {"current_floor": self.menara_game.lantai_sekarang.data.get("no_lantai")}
        save_data["inventory"] = self.inventory
        save_load.save_game(json_path / "savegame.json", save_data)
        self.destroy()

    # ==================== LOBI UTAMA ====================
    def show_main_lobby(self):
        self.clear_container()
        lbl_title = ctk.CTkLabel(self.container, text="LOBI UTAMA", font=("Arial", 32, "bold"))
        lbl_title.pack(pady=40)
        
        btn_summon = ctk.CTkButton(self.container, text="Summon Hall (Gacha)", font=("Arial", 18), height=50, command=self.show_summon_hall)
        btn_summon.pack(pady=10, fill="x", padx=200)
        
        btn_barrack = ctk.CTkButton(self.container, text="Barrack (Atur Pasukan)", font=("Arial", 18), height=50, command=self.show_barrack)
        btn_barrack.pack(pady=10, fill="x", padx=200)
        
        btn_tower = ctk.CTkButton(self.container, text="Tower Gate (Bertarung)", font=("Arial", 18), height=50, command=self.show_tower_gate)
        btn_tower.pack(pady=10, fill="x", padx=200)
        
        btn_quit = ctk.CTkButton(self.container, text="Simpan & Keluar", font=("Arial", 18), height=50, fg_color="#C62828", hover_color="#8E0000", command=self.save_and_quit)
        btn_quit.pack(pady=40, fill="x", padx=200)

    # ==================== SUMMON HALL ====================
    def show_summon_hall(self):
        self.clear_container()
        lbl_title = ctk.CTkLabel(self.container, text="SUMMON HALL", font=("Arial", 28, "bold"))
        lbl_title.pack(pady=20)
        
        lbl_tiket = ctk.CTkLabel(self.container, text=f"TIKET GACHA: {self.inventory.get('tiket_gacha', 0)}x", font=("Arial", 16))
        lbl_tiket.pack(pady=10)
        
        def gacha_10x():
            if self.inventory.get("tiket_gacha", 0) > 0:
                self.inventory["tiket_gacha"] -= 1
                for _ in range(10):
                    self.antrean_gacha.enqueue(f"Karakter_{random.randint(1000, 9999)}")
                messagebox.showinfo("Gacha Berhasil", "10 Karakter ditambahkan ke Antrean Klaim!")
                self.show_summon_hall()
            else:
                messagebox.showwarning("Tiket Habis", "Anda tidak memiliki Tiket Gacha!")
        
        btn_gacha = ctk.CTkButton(self.container, text="Tarik 10x Hero Baru", height=40, command=gacha_10x)
        btn_gacha.pack(pady=10)
        
        def klaim_antrean():
            if self.antrean_gacha.is_empty():
                messagebox.showinfo("Antrean Kosong", "Tidak ada hero untuk diklaim.")
                return
            
            dapat = []
            id_dalam_antrean = set()
            while not self.antrean_gacha.is_empty():
                item = self.antrean_gacha.dequeue()
                hasil = proses_gacha(id_dalam_antrean)
                if hasil:
                    h_id, hero_obj = hasil
                    barrack_aktif[h_id] = hero_obj
                    dapat.append(f"{hero_obj.nama} ({hero_obj.star_level}⭐)")
            
            hasil_teks = "\n".join(dapat)
            messagebox.showinfo("Hasil Klaim", f"Anda mendapatkan:\n{hasil_teks}")
            self.show_summon_hall()
            
        btn_klaim = ctk.CTkButton(self.container, text=f"Klaim Semua Antrean ({self.antrean_gacha.size()})", height=40, fg_color="#FBC02D", text_color="black", hover_color="#F9A825", command=klaim_antrean)
        btn_klaim.pack(pady=10)
        
        btn_back = ctk.CTkButton(self.container, text="Kembali", fg_color="gray", command=self.show_main_lobby)
        btn_back.pack(pady=30)

    # ==================== BARRACK ====================
    def show_barrack(self):
        self.clear_container()
        lbl_title = ctk.CTkLabel(self.container, text="BARRACK", font=("Arial", 28, "bold"))
        lbl_title.pack(pady=20)
        
        btn_daftar = ctk.CTkButton(self.container, text="1. Daftar Hero", height=40, command=self.show_daftar_hero)
        btn_daftar.pack(pady=10, fill="x", padx=250)
        
        btn_party = ctk.CTkButton(self.container, text="2. Atur Party", height=40, command=self.show_atur_party)
        btn_party.pack(pady=10, fill="x", padx=250)
        
        btn_evolusi = ctk.CTkButton(self.container, text="3. Ruang Evolusi & Sintesis", height=40, command=self.show_ruang_evolusi)
        btn_evolusi.pack(pady=10, fill="x", padx=250)
        
        btn_back = ctk.CTkButton(self.container, text="Kembali", fg_color="gray", command=self.show_main_lobby)
        btn_back.pack(pady=30)

    def show_daftar_hero(self):
        self.clear_container()
        lbl_title = ctk.CTkLabel(self.container, text="DAFTAR HERO", font=("Arial", 24, "bold"))
        lbl_title.pack(pady=10)
        
        scroll = ctk.CTkScrollableFrame(self.container, width=600, height=400)
        scroll.pack(pady=10)
        
        kumpulan_hero = list(barrack_aktif.values())
        if not kumpulan_hero:
            ctk.CTkLabel(scroll, text="Barrack Kosong...").pack(pady=20)
        else:
            for hero in kumpulan_hero:
                teks = f"[{hero.id}] {hero.nama} ({hero.star_level}⭐) | Lv.{hero.level}/{hero.max_level} | HP:{hero.hp} ATK:{hero.attack}"
                ctk.CTkLabel(scroll, text=teks).pack(anchor="w", pady=2)
                
        btn_back = ctk.CTkButton(self.container, text="Kembali", fg_color="gray", command=self.show_barrack)
        btn_back.pack(pady=10)

    def show_atur_party(self):
        self.clear_container()
        lbl_title = ctk.CTkLabel(self.container, text="ATUR PARTY", font=("Arial", 24, "bold"))
        lbl_title.pack(pady=10)
        
        lbl_party = ctk.CTkLabel(self.container, text="Anggota Party Saat Ini:", font=("Arial", 16))
        lbl_party.pack(pady=5)
        
        anggota = self.daftar_party["Party 1"]
        for i in range(5):
            peran = "KAPTEN" if i == 0 else f"Anggota {i}"
            nama = "Kosong"
            if i < len(anggota):
                h_id = anggota[i]
                if h_id in barrack_aktif:
                    nama = barrack_aktif[h_id].nama
            ctk.CTkLabel(self.container, text=f"{peran}: {nama}").pack()
            
        def reset_party():
            self.daftar_party["Party 1"] = []
            self.show_atur_party()
            
        def tambah_anggota():
            dialog = ctk.CTkInputDialog(text="Masukkan ID Hero yang ingin ditambahkan:", title="Tambah Anggota")
            h_id = dialog.get_input()
            if h_id:
                h_id = h_id.upper()
                if h_id in barrack_aktif:
                    if h_id not in self.daftar_party["Party 1"]:
                        if len(self.daftar_party["Party 1"]) < 5:
                            self.daftar_party["Party 1"].append(h_id)
                            self.show_atur_party()
                        else:
                            messagebox.showwarning("Penuh", "Party maksimal 5 anggota!")
                    else:
                        messagebox.showwarning("Duplikat", "Hero sudah ada di party!")
                else:
                    messagebox.showerror("Tidak Ditemukan", "ID Hero tidak valid!")
                    
        btn_tambah = ctk.CTkButton(self.container, text="Tambah Anggota (Via ID)", command=tambah_anggota)
        btn_tambah.pack(pady=10)
        
        btn_reset = ctk.CTkButton(self.container, text="Kosongkan Party", fg_color="red", command=reset_party)
        btn_reset.pack(pady=10)
        
        btn_back = ctk.CTkButton(self.container, text="Kembali", fg_color="gray", command=self.show_barrack)
        btn_back.pack(pady=10)

    def show_ruang_evolusi(self):
        self.clear_container()
        lbl_title = ctk.CTkLabel(self.container, text="RUANG EVOLUSI", font=("Arial", 24, "bold"))
        lbl_title.pack(pady=10)
        
        inv_frame = ctk.CTkFrame(self.container)
        inv_frame.pack(pady=10, fill="x", padx=100)
        
        kristal_str = " | ".join([f"{NAMA_KRISTAL[i]}:{self.inventory['kristal'].get(i,0)}" for i in range(1,8)])
        ctk.CTkLabel(inv_frame, text="Koleksi Kristal: " + kristal_str, font=("Arial", 12)).pack(pady=10)
        
        def evolusi_hero():
            dialog = ctk.CTkInputDialog(text="Masukkan ID Hero untuk dievolusi:", title="Evolusi")
            h_id = dialog.get_input()
            if h_id:
                h_id = h_id.upper()
                if h_id in barrack_aktif:
                    hero = barrack_aktif[h_id]
                    if hero.level >= hero.max_level and hero.star_level < 7:
                        butuh = hero.star_level + 1
                        if self.inventory["kristal"].get(butuh, 0) >= 1:
                            self.inventory["kristal"][butuh] -= 1
                            hero.evolusi()
                            messagebox.showinfo("Berhasil", f"{hero.nama} berhasil dievolusi ke {hero.star_level}⭐!")
                            self.show_ruang_evolusi()
                        else:
                            messagebox.showerror("Gagal", f"Butuh 1 Kristal {NAMA_KRISTAL[butuh]}!")
                    else:
                        messagebox.showerror("Gagal", "Belum Max Level atau sudah Bintang 7!")
                else:
                    messagebox.showerror("Error", "ID tidak ditemukan.")
                    
        def sintesis():
            dialog_lvl = ctk.CTkInputDialog(text="Level target (2-7):", title="Sintesis")
            lvl = dialog_lvl.get_input()
            if lvl and lvl.isdigit() and 2 <= int(lvl) <= 7:
                lvl = int(lvl)
                dialog_jml = ctk.CTkInputDialog(text="Jumlah sintesis:", title="Sintesis")
                jml = dialog_jml.get_input()
                if jml and jml.isdigit() and int(jml) > 0:
                    jml = int(jml)
                    butuh = jml * 5
                    sisa = self.inventory["kristal"].get(lvl-1, 0)
                    if sisa >= butuh:
                        self.inventory["kristal"][lvl-1] -= butuh
                        self.inventory["kristal"][lvl] = self.inventory["kristal"].get(lvl, 0) + jml
                        messagebox.showinfo("Berhasil", f"Disintesis {jml} Kristal {NAMA_KRISTAL[lvl]}!")
                        self.show_ruang_evolusi()
                    else:
                        messagebox.showerror("Gagal", f"Butuh {butuh} Kristal {NAMA_KRISTAL[lvl-1]}, hanya punya {sisa}.")
        
        btn_evo = ctk.CTkButton(self.container, text="Evolusi Hero", command=evolusi_hero)
        btn_evo.pack(pady=10)
        
        btn_sintesis = ctk.CTkButton(self.container, text="Sintesis Kristal", command=sintesis)
        btn_sintesis.pack(pady=10)
        
        btn_back = ctk.CTkButton(self.container, text="Kembali", fg_color="gray", command=self.show_barrack)
        btn_back.pack(pady=30)

    # ==================== TOWER GATE ====================
    def show_tower_gate(self):
        self.clear_container()
        lbl_title = ctk.CTkLabel(self.container, text="TOWER GATE", font=("Arial", 28, "bold"))
        lbl_title.pack(pady=20)
        
        if not self.daftar_party["Party 1"]:
            ctk.CTkLabel(self.container, text="Party Anda Kosong! Siapkan di Barrack terlebih dahulu.", text_color="red").pack(pady=20)
            btn_back = ctk.CTkButton(self.container, text="Kembali", fg_color="gray", command=self.show_main_lobby)
            btn_back.pack(pady=10)
            return

        lantai_data = self.menara_game.lantai_sekarang.data
        ctk.CTkLabel(self.container, text=f"Lantai Saat Ini: {lantai_data['no_lantai']} - {lantai_data['nama_lokasi']}", font=("Arial", 18)).pack(pady=10)
        
        self.log_box = ctk.CTkTextbox(self.container, width=800, height=350, state="disabled")
        self.log_box.pack(pady=10)
        
        def log_msg(msg):
            self.log_box.configure(state="normal")
            self.log_box.insert(ctk.END, msg + "\n")
            self.log_box.see(ctk.END)
            self.log_box.configure(state="disabled")
            self.update()
            
        def mulai_tarung():
            btn_tarung.configure(state="disabled")
            btn_back.configure(state="disabled")
            log_msg("=== PERTEMPURAN DIMULAI ===")
            
            # Setup Party Node
            master_party_node = RaidNode(Entity("Master Player", hp=999, attack=999), "Master Player")
            for h_id in self.daftar_party["Party 1"]:
                hero_obj = barrack_aktif[h_id]
                if hero_obj.is_alive:
                    h_node = RaidNode(hero_obj, "Hero")
                    master_party_node.tambah_unit(h_node)
                    
            if len(master_party_node.children) == 0:
                log_msg("[!] Semua hero di party sudah mati! Silakan ganti hero.")
                btn_tarung.configure(state="normal")
                btn_back.configure(state="normal")
                return
                
            # Setup Musuh Node
            master_musuh_node = RaidNode(Entity("Master Musuh", hp=999, attack=999), "Master Musuh")
            for m_id in lantai_data['id_musuh']:
                cek_boss = "BOSS" in m_id 
                if m_id in Daftar_Musuh:
                    b = Daftar_Musuh[m_id]
                    m_entity = Enemy(nama=b["name"], hp=b["hp"], atk=b["atk"], is_boss=cek_boss)
                else:
                    m_entity = Enemy(nama=m_id, hp=500 if cek_boss else 50, atk=150 if cek_boss else 15, is_boss=cek_boss)
                master_musuh_node.tambah_unit(RaidNode(m_entity, "Monster"))
                
            # Arena
            arena_cll = CircularLinkedList()
            arena_cll.append(master_party_node)
            arena_cll.append(master_musuh_node)
            
            # Combat Loop
            ronde = 1
            current = arena_cll.head
            while True:
                log_msg(f"\n--- Ronde {ronde} ---")
                penyerang = current.data
                bertahan = current.next.data
                
                log_msg(f"{penyerang.entity.nama} menyerang {bertahan.entity.nama}!")
                penyerang.serang_semua(bertahan)
                time.sleep(0.5)
                
                # Check status
                if len(bertahan.children) == 0:
                    if bertahan.role == "Master Musuh":
                        log_msg("\n[WIN] Pasukan Musuh Hancur! Kamu Menang!")
                        # Hadiah
                        hadiah_xp = lantai_data['no_lantai'] * 15
                        if lantai_data['is_boss']: hadiah_xp *= 10
                        log_msg(f"Mendapatkan {hadiah_xp} EXP!")
                        
                        is_first_clear = (lantai_data['no_lantai'] == self.menara_game.lantai_sekarang.data['no_lantai'] and not self.inventory.get("tamat", False))
                        if lantai_data['is_boss'] and is_first_clear:
                            self.inventory["tiket_gacha"] = self.inventory.get("tiket_gacha", 0) + 1
                            log_msg("🎉 BONUS BOSS: Mendapatkan 1x Tiket Gacha!")
                            
                        # Apply EXP
                        for anak in penyerang.children:
                            anak.data.entity.exp += hadiah_xp
                            if anak.data.entity.exp >= anak.data.entity.exp_next:
                                anak.data.entity.level_up()
                                log_msg(f"⭐ {anak.data.entity.nama} Level UP!")
                                
                        if self.menara_game.NaikLantai():
                            log_msg(f"\n[+] PROGRESS: Naik ke Lantai {self.menara_game.lantai_sekarang.data['no_lantai']}")
                        else:
                            self.inventory["tamat"] = True
                            log_msg("\n[+] TOWER CLEARED! Kamu mencapai puncak menara!")
                    else:
                        log_msg("\n[DEFEAT] Party kamu hancur lebur!")
                        for anak in bertahan.children:
                            anak.data.entity.is_alive = False
                    break
                    
                current = current.next
                ronde += 1
                if ronde > 50:
                    log_msg("Pertarungan terlalu lama. DRAW!")
                    break
                    
            btn_tarung.configure(state="normal")
            btn_back.configure(state="normal")
            
        btn_tarung = ctk.CTkButton(self.container, text="Maju! (Start Combat)", height=50, fg_color="#D84315", hover_color="#BF360C", command=mulai_tarung)
        btn_tarung.pack(pady=10)
        
        btn_back = ctk.CTkButton(self.container, text="Kembali", fg_color="gray", command=self.show_main_lobby)
        btn_back.pack(pady=10)

if __name__ == "__main__":
    app = PickMeUpGame()
    app.mainloop()
