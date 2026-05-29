Penjelasan Projek Pick Me Up: Cheap Edition

Kelompok 1 TI-B:
Islam Rahmatan Lil`Alamin
RAY DAVE ADONIA SIAGIAN
M. ABIYYU AL SAMY

1.	Deskripsi Projek
Pick Me Up: Cheap Edition adalah sebuah Role Playing Game (RPG) berbasis terminal yang mengadapasi konsep tower climbing dan manajemen karakter. Dalam permainian ini permain akan pbertindak sebagai “Master” yang bertugas mengelola sekumpulan kelompok untuk menaklukkan 100 lantai tower. 
2.	Mekanisme Game
Permainian ini mencakup beberapafitur utama yang salih berhubungan, yaitu:
•	Sistem Menara:  Menara terdiri dari 100 lantai, pemain mulai dari lantai 1 dan harus mengalahkan monster atau menyelesaikan quest tertentu untuk bisa naik ke lantai berikutnya, pemain boleh turun ke lantai yang sudah di taklukkan untuk farming resource atau leveling
•	Sistem Gacha: Pemain dapat memanggil hero dengan kelangkaan bintang 1 sampai 5 dan setiap hero memiliki batas maksimal level sesuai dengan bintangnya
•	Evolusi Karakter: Hero dapat dinaikkan bintangnya hingga maksimal 7 bintang dengan kristal evolusi yang berbeda-beda di tiap bnitangnya
•	Manajemen Party: pemain dapat menyusun party (tim) yang terdiri dari 1 hingga 5 orang. Untuk lantai khusus seperti boss raid (Kelipatan 5), pemain mungkin memerlukan beberapa party untuk menaklukkannya
•	Eksplorasi: pemain dapat mengirim hero untuk melakukan eksplorasi otomatis guna mencari resource tanpa harus mengontrolnya secara manual 
3.	Implementasi Struktur Data
•	Single Linked List: Struktur Menara 100 Lantai. Memungkinkan navigasi maju (lantai baru) dan mundur (untuk lantai yg sudah ditaklukkan)
•	Double Linked List: Sistem Eksplorasi otomatis rute ekspedisi satu arah melalui beberapa titik atau tempat
•	Circular Linked List: Sistem pertarungan Turn Based, mengatur giliran menyerangantara hero dan musuh secara berulang sampai dikalahkan
•	Graph: Navigasi Lobi Utama. Menghubungkan berbagai lokasi seperti Summon Hall, Barrack, dan Tower.
•	Tree: Sistem Multi-Party Raid. Mengelola hierarki kepemimpinan dan anggota tim saat melawan Bos besar.
•	Stack: Fitur Undo ketika ingin membatalkan Crafting Item selama item masih di antrian pembuatan.
•	Queue: Antrean Hasil Sumon. Memproses hero yang didapatkan dari gacha secara berurutan.
•	Hash Table: Database Hero dan item, digunakan untuk pencarian datasecara cepat.
•	Tipe data dasar: List (Inventory), Tuple (Koordinat & Probabilitas), Set (Koleksi), Dictionary (Atribut Karakter).

4.	Implementasi Algoritma
•	Sorting: Implementasi Quick Sort atau Merge Sort untuk mengurutkan daftar hero di Barrack berdasarkan Alfabet, level, bintang, atau kekuatan.
•	Searching: Implementasi Binary Search untuk mencari hero atau item spesifik dalam koleksi yang sudah terurut.
•	Rekursif:  Fungsi menghitung jumlah total kristal dasar yang dibutuhkan untuk menghasilkan kristal tingkat tinggi melalui beberapa tahap konversi.
•	File Handling: Sistem penyimpanan data untuk mencatat progres pemain, termasuk daftar hero, jumlah kristal, dan lantai menara yang telah dicapai.
•	OOP: Digunakan untuk membuat Class Enemy, Item, maupun Hero

