import json

# Algoritma Rekursi untuk menghitung kebutuhan Kristal Evolusi

def hitung_kebutuhan_kristal(level_awal, level_target, jumlah_target=1):
    """
    Fungsi rekursif untuk menghitung total kristal level rendah yang dibutuhkan 
    untuk membuat kristal level yang lebih tinggi.
    Setiap kenaikan 1 level membutuhkan 5 buah kristal dari level sebelumnya.
    """
    if level_awal == level_target:
        return jumlah_target
        
    if level_awal > level_target:
        return 0 # Tidak bisa memecah kristal (downgrade)
        
    return hitung_kebutuhan_kristal(level_awal, level_target - 1, jumlah_target * 5)
