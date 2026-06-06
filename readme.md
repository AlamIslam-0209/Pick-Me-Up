# 🏰 Pick Me Up: Cheap Edition

> **Sebuah Role Playing Game (RPG) Berbasis Terminal yang menggabungkan petualangan Tower Climbing dengan implementasi Struktur Data Kompleks secara *Real-Time*.**

Dibuat sebagai Proyek Akhir Algoritma dan Struktur Data oleh **Kelompok 1 TI-B**:
- Islam Rahmatan Lil'Alamin
- Ray Dave Adonia Siagian
- M. Abiyyu Al Samy

---

## 🎮 Panduan Bermain (Tutorial)

Game ini berbasis teks/terminal (CLI). Anda berperan sebagai *"Master"* yang bertugas mengelola pasukan pahlawan untuk menaklukkan puncak menara. Berikut adalah fitur-fitur yang bisa Anda jelajahi:

### 1. 🏛️ Lobi Utama
Pusat kendali permainan. Dari menu ini, Anda dapat memantau status posisi saat ini dan berpindah ke area utama lainnya seperti **Summon Hall** (Gacha), **Barrack** (Pengelolaan Pasukan), atau **Tower Gate** (Medan Tempur).

### 2. ✨ Summon Hall (Gacha)
Tempat Anda mengundi (Gacha) untuk menarik pahlawan baru menggunakan Tiket Gacha. 
- Pahlawan yang ditarik akan masuk ke dalam **Antrean**. 
- Anda harus mengklaim pahlawan tersebut secara berurutan agar mereka resmi masuk ke inventori Anda.

### 3. ⚔️ Barrack & Ruang Evolusi
Markas utama tempat pahlawan beristirahat. Fitur yang tersedia:
- **Daftar Hero**: Melihat semua pahlawan dengan algoritma pengurutan (*Sorting*).
- **Pencarian Hero**: Mencari pahlawan spesifik berdasarkan ID atau Nama (*Searching*).
- **Atur Party**: Menyusun formasi tempur (hingga 5 orang per regu).
- **Ruang Evolusi**: Menaikkan bintang (maks. 7⭐) menggunakan kristal, serta menyintesis kristal dengan kalkulator Rekursi.

### 4. 🧗‍♂️ Tower Climbing
Tantangan utama game: Memanjat 100 Lantai Menara. 
- Di setiap lantai, Anda bisa bertarung melawan monster untuk mendapatkan EXP. 
- Pada kelipatan 5 lantai, Anda akan melawan **Boss** dan diizinkan membawa hingga 2 *Party* (pasukan) sekaligus.
- Anda bebas turun ke lantai bawah yang sudah ditaklukkan untuk *farming* (mencari poin).

### 5. 🗺️ Ekspedisi Otomatis
Jika Anda memiliki hero yang sedang menganggur, Anda dapat mengirim mereka menyusuri peta (*Map*) secara otomatis.
- Pilih rute perjalanan secara manual dari titik ke titik.
- Waktu perjalanan bersifat *real-time* (berjalan di belakang layar terminal). Hero akan otomatis kembali setelah durasinya selesai.

---

## 💻 Implementasi Struktur Data

Di balik layar, *Pick Me Up: Cheap Edition* mengimplementasikan berbagai struktur data dinamis secara terintegrasi. Berbeda dengan rancangan awal, implementasi berikut adalah fakta aktual yang beroperasi di dalam baris kode:

### 📚 1. Riwayat Navigasi Menu (`Stack`)
Digunakan untuk merekam jejak menu layar (*Screen Navigation*). Beroperasi dengan prinsip LIFO (*Last In, First Out*). Saat Anda pindah dari Lobi ke Barrack, sistem melakukan `push("Barrack")`. Saat Anda memilih menu Kembali, sistem melakukan `pop()`.
```python
navigasi = Stack()
navigasi.push("Lobi Utama")
# Pindah menu -> navigasi.push("Barrack")
# Kembali -> navigasi.pop()
```

### ↕️ 2. Arsitektur Menara (`Double Linked List`)
Setiap lantai menara adalah sebuah *Node* yang saling terhubung ke lantai atas (`next`) dan lantai bawah (`prev`). Struktur ini menjamin pemain dapat berpindah lantai secara vertikal ke kedua arah secara mulus.
```python
class DoubleLinkedList:
    def NaikLantai(self):
        if self.lantai_sekarang and self.lantai_sekarang.next:
            self.lantai_sekarang = self.lantai_sekarang.next
            return True
            
    def TurunLantai(self):
        if self.lantai_sekarang and self.lantai_sekarang.prev:
            self.lantai_sekarang = self.lantai_sekarang.prev
            return True
```

### 🔗 3. Peta & Ekspedisi (`Single Linked List` & `Graph`)
- **Graph:** Peta dunia dikonstruksi menggunakan tipe *Graph* berbasis *Adjacency List*.
- **Single Linked List (SLL):** Digunakan ganda. Pertama, SLL menyusun senarai tetangga (tujuan lokasi) di setiap titik *Graph*. Kedua, lintasan Ekspedisi Pahlawan terekam menggunakan SLL agar berjalan satu arah (one-way).
```python
class Graph:
    def __init__(self):
        self.adj_list = {} # Berisi Single Linked List

    def tambah_jalan(self, asal, tujuan, waktu=0):
        self.adj_list[asal].tambah_di_akhir(tujuan, waktu)
```

### 🔄 4. Pertempuran Turn-Based (`Circular Linked List`)
Sistem pertarungan bergilir sirkular diatur oleh *Circular Linked List*. Ekor (*tail*) dari daftar tempur menunjuk kembali ke kepala (*head*), menciptakan pusaran pertempuran tanpa henti hingga salah satu entitas gugur.
```python
arena_cll = CircularLinkedList()
# Saat bertarung:
node_sekarang = node_sekarang.next # Terus berputar dari hero ke musuh kembali ke hero
```

### 🌳 5. Formasi Pasukan (`Tree`)
Hierarki pertempuran masif (Boss Raid) dikelola secara berjenjang menggunakan pola Pohon (*Tree*). Terdapat hierarki peran di mana "Master" membawahi "Kapten" formasi, dan "Kapten" menaungi beberapa unit "Anggota".
```python
kapten_node = RaidNode(kapten_obj, "Kapten")
anggota_node = RaidNode(anggota_obj, "Anggota")
kapten_node.tambah_unit(anggota_node) # Anggota menjadi child dari Kapten
```

### 📦 6. Database & Antrean (`Hash Table` & `Queue`)
- **Hash Table:** Menampung 100% *Blueprint* data hero. Mekanisme Kunci-Nilai mengubah pencarian spesifik menjadi berkecepatan absolut O(1).
- **Queue (Antrean):** Karakter hasil tarikan *gacha* ditumpuk sementara di *Queue* dan dikeluarkan secara adil menggunakan metode FIFO (*First In, First Out*).
```python
# Hash Table Database
Daftar_Hero = HashTable(400)
pencarian = Daftar_Hero.cari("H005")

# Queue Antrean Gacha
antrean_gacha = Queue()
antrean_gacha.enqueue(hero_baru) 
hero_diklaim = antrean_gacha.dequeue()
```

### 🛠️ 7. Tipe Data Lanjutan (`Dictionary, Set, Tuple, List`)
- `Dictionary`: Dipakai untuk manajemen *Save Game*, *Inventory*, dan *Ekspedisi Aktif*.
- `Set`: Mengelola ID Pahlawan di area Makam (*Graveyard*) agar tidak ada data kematian ganda.
- `Tuple`: Digunakan secara otomatis (implisit) saat fungsi *Tuple Unpacking* pada `enumerate()` dan operasi perulangan `.items()`.

---
*Game ini adalah bukti nyata bahwa sebaris teks kode mampu menghidupkan dunia petualangan tanpa batas ketika struktur datanya direkayasa dengan cermat!*
