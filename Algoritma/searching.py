def binary_search_hero_by_id(kumpulan_hero, target_id):
    """
    Mencari hero pakai teknik Binary Search berdasarkan ID.
    Ibarat nyari kata di kamus: kita buka bagian tengah dulu, kalau ID yang dicari
    lebih besar, cari di separuh kanan. Kalau lebih kecil, cari di separuh kiri.
    
    PENTING: List hero wajib udah berurutan (disorting) berdasarkan ID ya biar nggak nyasar!
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
    Mencari hero berdasarkan Nama pakai Binary Search.
    Sama kayak fungsi di atas, tapi patokannya adalah nama hero.
    Santai aja mau ngetik huruf besar atau kecil, tetep bakal nyambung (case-insensitive).
    
    PENTING: Pastiin list hero udah di-sorting menurut abjad dulu sebelum manggil ini!
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
    Mencari hero berdasarkan ID pakai gaya paling nyantai: dicek satu-satu dari awal sampai akhir!
    Sangat cocok dipakai kalau list hero lagi acak-acakan (belum di-sorting).
    """
    for hero in kumpulan_hero:
        if hero.id == target_id:
            return hero
    return None

def linear_search_hero_by_name(kumpulan_hero, target_name):
    """
    Mencari hero berdasarkan Nama, dicek satu-satu secara urut (Linear Search).
    Bisa dipakai kapan aja walau list heronya belum berurutan.
    Aman buat huruf besar/kecil.
    """
    target_name_lower = target_name.lower()
    for hero in kumpulan_hero:
        if hero.nama.lower() == target_name_lower:
            return hero
    return None
