import json
import random
import sys
import os
from pathlib import Path

from Entities.hero import Hero
from Entities.enemy import Enemy 
from Entities.entity import Entity
from StrukturData.Tree import RaidNode
from StrukturData.HashTable import HashTable
from StrukturData.Tower.Combat import CircularLinkedList, jalankan_raid_kombat
from StrukturData.Tower.MainTower import siapkan_menara

ROOT_DIR = Path(__file__).resolve().parent
json_path = ROOT_DIR / "data"

from Algoritma import save_load

barrack_aktif = {} # Menyimpan hero yang sedang aktif di barrack
graveyard = set() # Menyimpan ID hero yang telah mati
Daftar_Hero = HashTable(400) # Hash Table untuk menyimpan data hero
Daftar_Musuh = {} # Dictionary untuk menyimpan data musuh, dengan ID sebagai key
n = 1 

NAMA_KRISTAL = {1: "Merah", 2: "Jingga", 3: "Kuning", 4: "Hijau", 5: "Biru", 6: "Nila", 7: "Ungu"}

def tampilkan_kristal(inventory):
    '''
    Menampilkan sisa kristal evolusi yang ada di dalam inventory pemain.
    '''
    print("\n=== INVENTORY KRISTAL EVOLUSI ===")
    for level in range(1, 8):
        nama = NAMA_KRISTAL[level]
        jumlah = inventory.get("kristal", {}).get(level, 0)
        print(f"Lv.{level} [{nama}]: {jumlah} buah")
    print("=================================")

def bersihkan_layar():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def muat_hero():
    '''
    Membaca data cetak biru (blueprint) hero dari file JSON 
    lalu menyimpannya ke dalam Hash Table agar mudah dicari.
    '''
    with open(json_path / "heroBlueprints.json", "r") as file:
        hero_data = json.load(file)
        
    for hero_id, hero_info in hero_data.items():
        Daftar_Hero.tambah(hero_id, hero_info)
        
    print(f"[Info] {len(hero_data)} Hero berhasil dimuat ke dalam Hash Table!")
    
def muat_musuh():
    '''
    Membaca dan menyiapkan data status musuh serta boss dari file JSON ke dalam Dictionary.
    '''
    try:
        with open(json_path / "blueprint_enemy.json", "r") as file:
            enemy_data = json.load(file)
            for enemy in enemy_data:
                Daftar_Musuh[enemy["id"]] = enemy
        print(f"[Info] {len(Daftar_Musuh)} Musuh & Boss berhasil dimuat!")
    except FileNotFoundError:
        print("[Error] blueprint_enemy.json tidak ditemukan!")
        
        
def proses_gacha(id_antrian):
    '''
    Melakukan undian (gacha) untuk mendapatkan hero baru secara acak.
    Sistem hanya akan memilih hero yang belum dimiliki pemain atau pahlawan yang sudah mati.
    Peluang mendapat bintang tinggi bergantung pada persentase bobot yang ditentukan.
    '''
    pool_bintang = {1: [], 2: [], 3: [], 4: [], 5: []}
    
    for hero_id, hero_data in Daftar_Hero.ambilsemua():
        if hero_id not in barrack_aktif and hero_id not in graveyard and hero_id not in id_antrian:
            bintang = hero_data['star_level']
            pool_bintang[bintang].append(hero_id)
            
    if all(len(pool) == 0 for pool in pool_bintang.values()):
        print("\nGACHA GAGAL: Semua pahlawan di dunia ini sudah terpanggil atau telah gugur.")
        return None

    bobot_dasar = {
        5: 0.5,   
        4: 1.5,   
        3: 5.0,   
        2: 20.0,  
        1: 73.0   
    }
    
    bintang_tersedia = []
    bobot_tersedia = []
    
    for bintang in range(1, 6):
        if len(pool_bintang[bintang]) > 0:
            bintang_tersedia.append(bintang)
            bobot_tersedia.append(bobot_dasar[bintang])
            
    bintang_terpilih = random.choices(bintang_tersedia, weights=bobot_tersedia, k=1)[0]
    
    id_terpilih = random.choice(pool_bintang[bintang_terpilih])
    data_mentah = Daftar_Hero.cari(id_terpilih)
    
    hero_baru = Hero(data_mentah)
    return hero_baru

def cek_kematian(daftar_party):
    '''
    Memeriksa hero yang sudah kehabisan HP. Jika ada yang gugur, 
    hero tersebut akan dipindahkan ke makam (Graveyard) dan dikeluarkan dari party.
    '''
    id_yang_mati = []
    
    for hero_id, hero_obj in barrack_aktif.items():
        if not hero_obj.is_alive:
            id_yang_mati.append(hero_id)
            
    for hero_id in id_yang_mati:
        nama = barrack_aktif[hero_id].nama
        print(f"MEMORIAL: {nama} telah dipindahkan ke Memory Hall. Kematiannya tak akan dilupakan ")
        graveyard.add(hero_id)
        del barrack_aktif[hero_id]
        
        for anggota in daftar_party.values():
            if hero_id in anggota:
                anggota.remove(hero_id)
                
def cek_status(node_party):
    '''
    Memeriksa kondisi HP setiap hero setelah pertarungan selesai.
    Akan menampilkan peringatan jika ada hero yang sekarat (HP 20% ke bawah).
    '''
    for anggota in node_party.anak:
        if anggota.entitas.is_alive and anggota.entitas.hp <= 0.2 * anggota.entitas.hp_max:
            print(f"⚠️  PERINGATAN: {anggota.entitas.nama} sekarat (HP: {anggota.entitas.hp}/{anggota.entitas.hp_max})")
        if anggota.peran in ["Master", "Kapten", "Anggota"]:
            cek_status(anggota)


def save_load_game(barrack_aktif, graveyard, daftar_party, menara_game, inventory, ekspedisi_aktif):
    '''
    Menyimpan semua data permainan saat ini (hero, party, posisi menara, dan inventory) ke file JSON.
    '''
    save_path = json_path / "savegame.json"
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
            "is_exploring": getattr(hero_obj, "is_exploring", False),
            "exp": getattr(hero_obj, "exp", 0),
            "exp_next": getattr(hero_obj, "exp_next", hero_obj.level*100)
        }
    save_data["graveyard"] = list(graveyard)
    save_data["daftar_party"] = daftar_party
    save_data["menara"] = {"current_floor": menara_game.lantai_sekarang.data.get("no_lantai")}
    if not inventory:
        inventory = {"tiket_gacha": 0, "kristal": {i: 0 for i in range(1, 8)}}
    save_data["inventory"] = inventory
    save_data["ekspedisi_aktif"] = ekspedisi_aktif
    save_load.save_game(save_path, save_data)
    
    
def cek_save_load(saved_data, graveyard, daftar_party, barrack_aktif, menara_game, inventory, ekspedisi_aktif):
    '''
    Memeriksa ketersediaan file penyimpanan (save data) saat game dimulai. 
    Jika file ditemukan, data permainan akan dimuat ulang. 
    Jika tidak, sistem akan menyiapkan nilai bawaan (default) untuk memulai permainan baru.
    '''
    if saved_data:
        print("[Info] Save data ditemukan! Memuat progress sebelumnya...")
        if "inventory" in saved_data:
            inventory["tiket_gacha"] = saved_data["inventory"].get("tiket_gacha", 0)
            
            loaded_kristal = saved_data["inventory"].get("kristal", {str(i): 0 for i in range(1, 8)})
            inventory["kristal"] = {int(k): v for k, v in loaded_kristal.items()}
            
            for i in range(1, 8):
                if i not in inventory["kristal"]:
                    inventory["kristal"][i] = 0
        else:
            inventory["tiket_gacha"] = 0
            inventory["kristal"] = {i: 0 for i in range(1, 8)}
        
        if "graveyard" in saved_data:
            graveyard.update(saved_data["graveyard"])
            
        if "daftar_party" in saved_data:
            daftar_party.clear()
            daftar_party.update(saved_data["daftar_party"])
            
        if "barrack_aktif" in saved_data:
            for h_id, h_data in saved_data["barrack_aktif"].items():
                data_mentah = Daftar_Hero.cari(h_data["id"])
                if data_mentah:
                    hero_baru = Hero(data_mentah)
                    hero_baru.hp = h_data["hp"]
                    hero_baru.hp_max = h_data.get("hp_max", hero_baru.hp_max)
                    hero_baru.attack = h_data.get("attack", hero_baru.attack)
                    hero_baru.level = h_data["level"]
                    hero_baru.star_level = h_data.get("star_level", hero_baru.star_level)
                    hero_baru.max_level = hero_baru.star_level * 20
                    hero_baru.exp = h_data.get("exp", 0)
                    hero_baru.exp_next = h_data.get("exp_next", hero_baru.level * 100)
                    hero_baru.is_alive = h_data["is_alive"]
                    hero_baru.is_exploring = h_data.get("is_exploring", False)
                    if "equipment" in h_data and "weapon" in h_data["equipment"]:
                        hero_baru.weapon = h_data["equipment"]["weapon"]
                    barrack_aktif[h_id] = hero_baru
                    
        if "menara" in saved_data:
            target_lantai = saved_data["menara"].get("current_floor", 1)
            current_node = menara_game.head
            while current_node:
                if current_node.data["no_lantai"] == target_lantai:
                    menara_game.lantai_sekarang = current_node
                    break
                current_node = current_node.next
                
        if "ekspedisi_aktif" in saved_data:
            ekspedisi_aktif.clear()
            ekspedisi_aktif.update(saved_data["ekspedisi_aktif"])
    else:
        print("[Info] Tidak ada save data. Memulai game baru...")
        inventory["tiket_gacha"] = 1
        inventory["kristal"] = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}
