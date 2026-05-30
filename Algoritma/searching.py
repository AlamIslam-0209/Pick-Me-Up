def binary_search_hero_by_id(kumpulan_hero, target_id):
    """
    Mencari hero berdasarkan ID menggunakan metode Binary Search.
    Pencarian dilakukan dengan membagi data menjadi dua bagian secara berulang.
    
    Catatan: Kumpulan hero harus sudah diurutkan berdasarkan ID sebelum memanggil fungsi ini.
    """
    left = 0
    right = len(kumpulan_hero) - 1
    
    while left <= right:
        mid = (left + right) // 2
        mid_id = kumpulan_hero[mid].id
        
        if mid_id == target_id:
            return kumpulan_hero[mid] # Yeay, ketangkep heronya!
        elif mid_id < target_id:
            left = mid + 1            # Geser area pencarian ke sebelah kanan
        else:
            right = mid - 1           # Geser area pencarian ke sebelah kiri
            
    return None # Yah, heronya nggak ada di list

def binary_search_hero_by_name(kumpulan_hero, target_name):
    """
    Mencari hero berdasarkan nama menggunakan metode Binary Search.
    Pencarian mengabaikan huruf besar dan kecil (case-insensitive).
    
    Catatan: Kumpulan hero harus sudah diurutkan secara abjad sebelum memanggil fungsi ini.
    """
    left = 0
    right = len(kumpulan_hero) - 1
    target_name_lower = target_name.lower() # Jadikan huruf kecil semua biar enak dicocokin
    
    while left <= right:
        mid = (left + right) // 2
        mid_name = kumpulan_hero[mid].nama.lower()
        
        if mid_name == target_name_lower:
            return kumpulan_hero[mid]
        elif mid_name < target_name_lower:
            left = mid + 1
        else:
            right = mid - 1
            
    return None

def linear_search_hero_by_id(kumpulan_hero, target_id):
    """
    Mencari hero berdasarkan ID dengan memeriksa data satu per satu dari awal.
    Metode ini cocok digunakan jika kumpulan hero belum diurutkan.
    """
    for hero in kumpulan_hero:
        if hero.id == target_id:
            return hero
    return None

def linear_search_hero_by_name(kumpulan_hero, target_name):
    """
    Mencari hero berdasarkan nama dengan memeriksa data satu per satu.
    Pencarian mengabaikan huruf besar dan kecil (case-insensitive).
    Bisa digunakan pada kumpulan hero yang belum diurutkan.
    """
    target_name_lower = target_name.lower()
    for hero in kumpulan_hero:
        if hero.nama.lower() == target_name_lower:
            return hero
    return None
