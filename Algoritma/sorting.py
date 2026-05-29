def _merge_sort(arr, key):
    """
    Fungsi inti dari Merge Sort. Cara kerjanya mirip seperti membagi tumpukan kartu:
    1. Bagi list hero menjadi dua bagian (kiri dan kanan) sampai tersisa 1 hero saja.
    2. Urutkan dan gabungkan kembali (merge) perlahan-lahan dari bawah ke atas.
    
    Argumen:
    - arr: List pahlawan/data yang mau diurutkan.
    - key: Fungsi kecil penentu patokan urutan (bisa ID, Nama, Level, dll).
    """
    if len(arr) <= 1:
        return arr[:]
        
    mid = len(arr) // 2
    left = _merge_sort(arr[:mid], key)
    right = _merge_sort(arr[mid:], key)
    
    merged = []
    i = j = 0
    
    # Proses penggabungan (merge): Bandingkan elemen paling depan dari kiri dan kanan
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
            
    # Masukkan sisa elemen jika salah satu sisi sudah habis duluan
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged

def sort_heroes_by_id(kumpulan_hero):
    """Bantu urutin list hero berdasarkan ID-nya (contoh: H001, H002) secara berurutan."""
    return _merge_sort(kumpulan_hero, key=lambda h: h.id)

def sort_heroes_by_name(kumpulan_hero):
    """Bantu urutin list hero secara abjad (A-Z) berdasarkan namanya. Huruf besar/kecil nggak ngaruh!"""
    return _merge_sort(kumpulan_hero, key=lambda h: h.nama.lower())

def sort_heroes_by_level(kumpulan_hero):
    """Bantu urutin list hero dari level paling rendah sampai level paling tinggi."""
    return _merge_sort(kumpulan_hero, key=lambda h: h.level)

def sort_heroes_by_star(kumpulan_hero):
    """Bantu urutin list hero dari bintang paling dikit sampai yang bintangnya mentok (paling tinggi)."""
    return _merge_sort(kumpulan_hero, key=lambda h: h.star_level)
