import sys
import os
from pathlib import Path

# --- Mengatur Path Otomatis ---
ROOT_DIR = Path(__file__).resolve().parent
sys.path.append(str(ROOT_DIR))

from StrukturData.Stack import Stack
from StrukturData.Queue import Queue # <-- Tambahkan baris ini
import random

def bersihkan_layar():
    """Fungsi biar terminal rapi setiap kali pindah menu"""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    # 1. Inisialisasi 
    antrean_gacha = Queue()
    navigasi = Stack()
    
    # 2. Masukkan menu pertama kali saat game dibuka (Push)
    navigasi.push("Lobi Utama")
    
    # 3. GAME LOOP (Game akan berjalan selama loop ini aktif)
    while True:
        bersihkan_layar()
        
        # Mengecek kita sedang berada di menu mana (Peek)
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
            print("3. Pergi ke Tower Gate (Panjat Menara)")
            print("0. Keluar dari Game")
            
            pilihan = input("> Pilih aksi (0-3): ")
            
            if pilihan == "1":
                navigasi.push("Summon Hall")  # Pindah menu = Push
            elif pilihan == "2":
                navigasi.push("Barrack")
            elif pilihan == "3":
                navigasi.push("Tower Gate")
            elif pilihan == "0":
                print("Menyimpan progres... Sampai jumpa, Master!")
                break # Keluar dari Game Loop (Game Over/Tutup)
            else:
                input("Pilihan tidak valid! (Tekan Enter untuk lanjut)")

        # ==========================================
        # LOGIKA MENU: BARRACK
        # ==========================================
        elif layar_sekarang == "Barrack":
            print("1. Lihat Daftar Hero (Sorting)")
            print("2. Cari Hero Spesifik (Searching)")
            print("0. KEMBALI ke Lobi Utama")
            
            pilihan = input("> Pilih aksi (0-2): ")
            
            if pilihan == "1":
                navigasi.push("Daftar Hero") # Pindah ke sub-menu yang lebih dalam
            elif pilihan == "2":
                navigasi.push("Cari Hero")
            elif pilihan == "0":
                navigasi.pop() # TOMBOL BACK = Pop menu Barrack, otomatis balik ke Lobi!

        # ==========================================
        # LOGIKA MENU: DAFTAR HERO (Sub-menu Barrack)
        # ==========================================
        elif layar_sekarang == "Daftar Hero":
            print("[Di sini nanti nyambungin algoritma Merge Sort Hero...]")
            print("\n0. KEMBALI ke Barrack")
            
            pilihan = input("> Pilih aksi: ")
            
            if pilihan == "0":
                navigasi.pop() # TOMBOL BACK = Pop menu Daftar Hero, otomatis balik ke Barrack!

        # ==========================================
        # LOGIKA MENU: SUMMON HALL
        # ==========================================
        elif layar_sekarang == "Summon Hall":
            # Menampilkan info antrean yang belum diklaim
            print(f"--- ANTREAN KLAIM: {antrean_gacha.size()} Hero Menunggu ---")
            if not antrean_gacha.is_empty():
                print(f"Hero selanjutnya: {antrean_gacha.front_item()}")
            print("-" * 45)
            
            print("1. Tarik 10x Hero Baru (Gacha)")
            print("2. Klaim 1 Hero dari Antrean")
            print("0. KEMBALI ke Lobi Utama")
            
            pilihan = input("> Pilih aksi: ")
            
            if pilihan == "1":
                # Simulasi gacha sederhana (Nanti ini kita hubungkan ke Hash Table)
                daftar_hero_sementara = ["Arthur (Bintang 5)", "Lancelot (Bintang 4)", "Goblin (Bintang 1)", "Slime (Bintang 1)"]
                
                print("\n[+] Menarik 10 Hero ke dalam antrean...")
                for _ in range(10):
                    hero_didapat = random.choice(daftar_hero_sementara)
                    antrean_gacha.enqueue(hero_didapat) # Masuk barisan belakang
                    
                input("Gacha selesai! 10 Hero telah masuk antrean. (Tekan Enter)")
                
            elif pilihan == "2":
                if antrean_gacha.is_empty():
                    input("\n[!] Antrean kosong! Kamu harus Gacha dulu. (Tekan Enter)")
                else:
                    # Mengeluarkan hero dari barisan paling depan
                    hero_diklaim = antrean_gacha.dequeue()
                    print(f"\n[!] SELAMAT! Kamu berhasil mengklaim: {hero_diklaim}")
                    input("Hero telah dimasukkan ke Inventory. (Tekan Enter)")
                    
            elif pilihan == "0":
                navigasi.pop() # Balik ke Lobi

# Menjalankan fungsi utama
if __name__ == "__main__":
    main()