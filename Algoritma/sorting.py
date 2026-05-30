def _merge_sort(arr, key):
    """
    Fungsi utama untuk mengurutkan data menggunakan algoritma Merge Sort.
    Data akan dibagi menjadi dua bagian secara terus-menerus, lalu digabungkan kembali secara berurutan.
    
    Argumen:
    - arr: List data yang ingin diurutkan.
    - key: Fungsi untuk menentukan atribut yang dijadikan patokan urutan (misalnya ID, nama, level).
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
    """Mengurutkan daftar hero berdasarkan ID mereka secara menaik."""
    return _merge_sort(kumpulan_hero, key=lambda h: h.id)

def sort_heroes_by_name(kumpulan_hero):
    """Mengurutkan daftar hero berdasarkan abjad dari nama mereka (case-insensitive)."""
    return _merge_sort(kumpulan_hero, key=lambda h: h.nama.lower())

def sort_heroes_by_level(kumpulan_hero):
    """Mengurutkan daftar hero dari level terendah hingga tertinggi."""
    return _merge_sort(kumpulan_hero, key=lambda h: h.level)

def sort_heroes_by_star(kumpulan_hero):
    """Mengurutkan daftar hero berdasarkan jumlah bintang dari yang terkecil hingga terbesar."""
    return _merge_sort(kumpulan_hero, key=lambda h: h.star_level)
