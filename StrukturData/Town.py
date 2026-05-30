import json
from pathlib import Path

import sys

if getattr(sys, 'frozen', False):
    ROOT_DIR = Path(sys.executable).parent
else:
    ROOT_DIR = Path(__file__).resolve().parent.parent
json_path = ROOT_DIR / "data"

class SLLNode:
    """Node khusus untuk Single Linked List yang merepresentasikan tujuan lokasi."""
    def __init__(self, nama_lokasi, waktu=0):
        self.lokasi = nama_lokasi
        self.waktu = waktu # Durasi waktu (dalam detik) untuk mencapai lokasi ini
        self.next = None

class SingleLinkedList:
    """Single Linked List untuk menyimpan daftar lokasi tujuan (Edge) secara berurutan."""
    def __init__(self):
        self.head = None

    def tambah_di_akhir(self, nama_lokasi, waktu=0):
        """Menambahkan tujuan baru ke akhir SLL."""
        node_baru = SLLNode(nama_lokasi, waktu)
        if self.head is None:
            self.head = node_baru
            return
        
        sekarang = self.head
        while sekarang.next:
            sekarang = sekarang.next
        sekarang.next = node_baru

    def ambil_semua(self):
        """Membaca isi SLL dari awal sampai akhir dan mengembalikan dalam bentuk list Python."""
        hasil = []
        sekarang = self.head
        while sekarang:
            hasil.append({"tujuan": sekarang.lokasi, "waktu": sekarang.waktu})
            sekarang = sekarang.next
        return hasil

class Graph:
    """Graph Adjacency List untuk menyimpan Peta Dunia (Town/Map)."""
    def __init__(self):
        self.adj_list = {}

    def tambah_lokasi(self, lokasi):
        """Mendaftarkan lokasi baru sebagai vertex di dalam Graph."""
        if lokasi not in self.adj_list:
            self.adj_list[lokasi] = SingleLinkedList()

    def tambah_jalan(self, asal, tujuan, waktu=0):
        """Membuat jalan penghubung (edge) berbobot waktu antara dua lokasi."""
        self.tambah_lokasi(asal)
        self.tambah_lokasi(tujuan)
            
        self.adj_list[asal].tambah_di_akhir(tujuan, waktu)

    def lihat_jalan(self, lokasi):
        """Mengambil semua jalan keluar (edges) dari lokasi saat ini lewat SLL."""
        if lokasi in self.adj_list:
            return self.adj_list[lokasi].ambil_semua()
        return []

def siapkan_peta():
    """Menginisialisasi Graph dan membentuk peta dunia (Rute Eksplorasi)."""
    peta = Graph()
    
    with open(json_path / "map.json", "r") as f:
        blueprint_rute = json.load(f)
    
    # Memasukkan blueprint dictionary ke dalam struktur Graph & Single Linked List
    for asal, daftar_tujuan in blueprint_rute.items():
        peta.tambah_lokasi(asal) # Memastikan lokasi asal terdaftar meski belum/tidak punya tujuan
        for item in daftar_tujuan:
            peta.tambah_jalan(asal, item["tujuan"], item["waktu"])
            
    return peta
