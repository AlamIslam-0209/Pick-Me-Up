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
