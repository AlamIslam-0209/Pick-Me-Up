import json

# Algoritma Rekursi untuk menghitung kebutuhan Kristal Evolusi

def hitung_kebutuhan_kristal(level_awal, level_target, jumlah_target=1):
    """
    Fungsi rekursif untuk menghitung berapa banyak kristal `level_awal` 
    yang dibutuhkan untuk membuat `jumlah_target` buah kristal `level_target`.
    Setiap naik 1 level membutuhkan 5 kristal level sebelumnya.
    """
    if level_awal == level_target:
        return jumlah_target
        
    if level_awal > level_target:
        return 0 # Tidak bisa memecah kristal (downgrade)
        
    return hitung_kebutuhan_kristal(level_awal, level_target - 1, jumlah_target * 5)
