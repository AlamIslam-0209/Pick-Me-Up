<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pick Me Up: Cheap Edition - Interactive Docs</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-main: #0B0E14;
            --bg-card: rgba(20, 25, 35, 0.6);
            --accent-primary: #8b5cf6;
            --accent-secondary: #06b6d4;
            --text-main: #e2e8f0;
            --text-muted: #94a3b8;
            --glass-border: rgba(255, 255, 255, 0.08);
            --glass-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            scroll-behavior: smooth;
        }

        body {
            font-family: 'Outfit', sans-serif;
            background-color: var(--bg-main);
            color: var(--text-main);
            line-height: 1.6;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 15% 50%, rgba(139, 92, 246, 0.15), transparent 25%),
                radial-gradient(circle at 85% 30%, rgba(6, 182, 212, 0.15), transparent 25%);
            background-attachment: fixed;
        }

        /* --- TYPOGRAPHY & LAYOUT --- */
        h1, h2, h3 { font-weight: 800; }
        
        .container {
            max-width: 1100px;
            margin: 0 auto;
            padding: 0 2rem;
        }

        /* --- HERO SECTION --- */
        .hero {
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            position: relative;
            animation: fadeIn 1.5s ease-out;
        }

        .hero h1 {
            font-size: 4.5rem;
            background: linear-gradient(to right, var(--accent-primary), var(--accent-secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
            filter: drop-shadow(0 0 20px rgba(139, 92, 246, 0.4));
        }

        .hero p {
            font-size: 1.2rem;
            color: var(--text-muted);
            max-width: 600px;
            margin-bottom: 2rem;
        }

        .btn {
            display: inline-block;
            padding: 1rem 2.5rem;
            font-size: 1.1rem;
            font-weight: 600;
            color: #fff;
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
            border: none;
            border-radius: 50px;
            text-decoration: none;
            cursor: pointer;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);
        }

        .btn:hover {
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 8px 25px rgba(6, 182, 212, 0.5);
        }

        /* --- SECTIONS --- */
        section {
            padding: 6rem 0;
            opacity: 0;
            transform: translateY(30px);
            transition: all 0.8s ease-out;
        }

        section.visible {
            opacity: 1;
            transform: translateY(0);
        }

        .section-title {
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 3rem;
            position: relative;
        }

        .section-title::after {
            content: '';
            display: block;
            width: 80px;
            height: 4px;
            background: var(--accent-secondary);
            margin: 0.5rem auto 0;
            border-radius: 2px;
        }

        /* --- CARDS (GLASSMORPHISM) --- */
        .grid-cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
        }

        .card {
            background: var(--bg-card);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 2rem;
            box-shadow: var(--glass-shadow);
            transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), border-color 0.3s;
        }

        .card:hover {
            transform: translateY(-10px);
            border-color: var(--accent-secondary);
        }

        .card h3 {
            font-size: 1.5rem;
            color: var(--accent-secondary);
            margin-bottom: 1rem;
        }

        .card p {
            color: var(--text-muted);
            font-size: 0.95rem;
        }

        /* --- INTERACTIVE TABS (IMPLEMENTASI KODE) --- */
        .tabs-container {
            display: flex;
            flex-direction: column;
            gap: 2rem;
        }

        .tab-buttons {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 1rem;
        }

        .tab-btn {
            background: var(--bg-card);
            border: 1px solid var(--glass-border);
            color: var(--text-main);
            padding: 0.8rem 1.5rem;
            border-radius: 30px;
            cursor: pointer;
            font-family: inherit;
            font-weight: 600;
            transition: all 0.3s ease;
        }

        .tab-btn:hover, .tab-btn.active {
            background: var(--accent-primary);
            border-color: var(--accent-primary);
            box-shadow: 0 0 15px rgba(139, 92, 246, 0.5);
            transform: translateY(-2px);
        }

        .tab-content {
            display: none;
            background: var(--bg-card);
            backdrop-filter: blur(12px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 2.5rem;
            animation: fadeIn 0.5s ease;
        }

        .tab-content.active {
            display: block;
        }

        .tab-content h3 {
            color: var(--accent-secondary);
            margin-bottom: 1rem;
            font-size: 1.8rem;
        }

        code {
            font-family: 'JetBrains Mono', monospace;
            background: rgba(0,0,0,0.5);
            padding: 0.2rem 0.4rem;
            border-radius: 4px;
            color: #fca5a5;
        }

        .code-block {
            background: #0d1117;
            padding: 1.5rem;
            border-radius: 10px;
            overflow-x: auto;
            margin-top: 1.5rem;
            border: 1px solid #30363d;
            color: #c9d1d9;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
        }

        /* --- ANIMATIONS --- */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* --- FOOTER --- */
        footer {
            text-align: center;
            padding: 3rem 0;
            border-top: 1px solid var(--glass-border);
            margin-top: 4rem;
            color: var(--text-muted);
        }

        /* Responsive */
        @media (max-width: 768px) {
            .hero h1 { font-size: 3rem; }
            .tab-buttons { flex-direction: column; }
            .tab-btn { width: 100%; text-align: center; }
        }
    </style>
</head>
<body>

    <!-- HERO SECTION -->
    <header class="hero">
        <div class="container">
            <h1>Pick Me Up</h1>
            <h3>Cheap Edition</h3>
            <p style="margin-top: 1rem;">Sebuah Role Playing Game (RPG) Berbasis Terminal yang menggabungkan petualangan Tower Climbing dengan implementasi Struktur Data Kompleks.</p>
            <a href="#tutorial" class="btn">Mulai Eksplorasi Docs</a>
        </div>
    </header>

    <!-- TUTORIAL SECTION -->
    <section id="tutorial" class="container">
        <h2 class="section-title">Panduan Bermain</h2>
        <div class="grid-cards">
            <div class="card">
                <h3>🏛️ Lobi Utama</h3>
                <p>Pusat kendali permainan. Dari sini Anda dapat berpindah ke <b>Summon Hall</b> untuk gacha pahlawan, ke <b>Barrack</b> untuk menyusun strategi, atau ke <b>Tower Gate</b> untuk memulai pertarungan dan ekspedisi.</p>
            </div>
            <div class="card">
                <h3>✨ Summon Hall (Gacha)</h3>
                <p>Tarik hingga 10 pahlawan secara acak menggunakan Tiket Gacha. Pahlawan yang didapat akan masuk ke dalam <b>Antrean</b> dan harus diklaim satu per satu agar masuk ke inventory Anda.</p>
            </div>
            <div class="card">
                <h3>⚔️ Barrack & Ruang Evolusi</h3>
                <p>Tempat memantau pahlawan, menyusun <b>Party (Formasi Tempur)</b> hingga 5 orang, serta melakukan evolusi tingkat bintang hero menggunakan Kristal yang didapat dari menara.</p>
            </div>
            <div class="card">
                <h3>🧗‍♂️ Tower Climbing</h3>
                <p>Tantang diri Anda memanjat 100 Lantai Menara. Hadapi monster biasa hingga <b>Boss</b> setiap kelipatan 5 lantai. Anda bisa kembali ke lantai bawah untuk <i>farming</i> EXP.</p>
            </div>
            <div class="card">
                <h3>🗺️ Ekspedisi Otomatis</h3>
                <p>Kirim pahlawan yang menganggur untuk menjelajahi peta dunia. Pilih rute lokasi secara manual, lalu biarkan mereka berpetualang dan kembali secara <i>real-time</i>.</p>
            </div>
        </div>
    </section>

    <!-- IMPLEMENTASI KODE SECTION -->
    <section id="kode" class="container">
        <h2 class="section-title">Implementasi Struktur Data</h2>
        <p style="text-align: center; color: var(--text-muted); margin-bottom: 2rem;">Game ini bukan sekadar permainan biasa, melainkan implementasi mahakarya arsitektur Struktur Data. Klik *tab* di bawah untuk mempelajari kodenya.</p>
        
        <div class="tabs-container">
            <div class="tab-buttons">
                <button class="tab-btn active" onclick="openTab(event, 'Stack')">Stack</button>
                <button class="tab-btn" onclick="openTab(event, 'DLL')">Double Linked List</button>
                <button class="tab-btn" onclick="openTab(event, 'SLL')">Single Linked List & Graph</button>
                <button class="tab-btn" onclick="openTab(event, 'CLL')">Circular Linked List</button>
                <button class="tab-btn" onclick="openTab(event, 'Tree')">Tree</button>
                <button class="tab-btn" onclick="openTab(event, 'Hash')">Hash Table & Queue</button>
            </div>

            <!-- Tab Content: Stack -->
            <div id="Stack" class="tab-content active">
                <h3>Riwayat Navigasi Menu (Stack)</h3>
                <p>Digunakan untuk merekam jejak menu layar (*Screen Navigation*). Beroperasi dengan prinsip LIFO (*Last In, First Out*). Saat Anda pindah dari Lobi ke Barrack, sistem melakukan <code>push("Barrack")</code>. Saat Anda kembali, sistem melakukan <code>pop()</code>.</p>
                <div class="code-block">
navigasi = Stack()
navigasi.push("Lobi Utama")

# Saat pindah ke menu lain
if pilihan == "2":
    navigasi.push("Barrack")

# Saat memilih KEMBALI
elif pilihan == "0":
    navigasi.pop() # Kembali ke Lobi Utama
                </div>
            </div>

            <!-- Tab Content: DLL -->
            <div id="DLL" class="tab-content">
                <h3>Arsitektur Menara (Double Linked List)</h3>
                <p>Setiap lantai menara adalah sebuah <i>Node</i> yang terhubung ke lantai atas <code>next</code> dan lantai bawah <code>prev</code>. Pemain dapat naik atau turun dengan mulus tanpa memutus rantai arsitektur.</p>
                <div class="code-block">
class DoubleLinkedList:
    def NaikLantai(self):
        if self.lantai_sekarang and self.lantai_sekarang.next:
            self.lantai_sekarang = self.lantai_sekarang.next
            return True
            
    def TurunLantai(self):
        if self.lantai_sekarang and self.lantai_sekarang.prev:
            self.lantai_sekarang = self.lantai_sekarang.prev
            return True
                </div>
            </div>

            <!-- Tab Content: SLL & Graph -->
            <div id="SLL" class="tab-content">
                <h3>Peta & Ekspedisi (Graph & Single Linked List)</h3>
                <p>Peta dunia dibentuk menggunakan struktur <b>Graph</b> berbasis <i>Adjacency List</i>. Setiap lokasi memegang sebuah <b>Single Linked List</b> yang berisi tujuan-tujuan yang bisa dituju. Selain itu, rute perjalanan hero ekspedisi berjalan satu arah menggunakan SLL.</p>
                <div class="code-block">
class Graph:
    def __init__(self):
        self.adj_list = {} # Menyimpan nama lokasi

    def tambah_jalan(self, asal, tujuan, waktu=0):
        # Menggunakan SLL untuk menampung edge (jalur)
        self.adj_list[asal].tambah_di_akhir(tujuan, waktu)
        
# Implementasi Rute Sekali Jalan
rute_ekspedisi = SingleLinkedList()
rute_ekspedisi.tambah_di_akhir("Hutan Gelap", 60)
                </div>
            </div>

            <!-- Tab Content: CLL -->
            <div id="CLL" class="tab-content">
                <h3>Pertempuran (Circular Linked List)</h3>
                <p>Sistem *Turn-Based Combat* bergilir diatur menggunakan <b>Circular Linked List</b>. Ekor (*tail*) dari daftar tempur menunjuk kembali ke kepala (*head*), menciptakan putaran giliran tak berujung hingga salah satu pihak kehabisan HP.</p>
                <div class="code-block">
# Di dalam Combat.py
arena_cll = CircularLinkedList()

# Pertarungan bergilir sirkular
while musuh_hidup > 0 and party_hidup > 0:
    penyerang = node_sekarang.data
    # Logika Serang...
    node_sekarang = node_sekarang.next # Pindah giliran terus berputar
                </div>
            </div>

            <!-- Tab Content: Tree -->
            <div id="Tree" class="tab-content">
                <h3>Formasi Pasukan (Tree / Pohon)</h3>
                <p>Hirarki pertempuran masif (*Boss Raid*) menggunakan struktur <b>Tree</b>. Entitas "Master" membawahi "Kapten" Party, dan setiap "Kapten" membawahi banyak unit "Anggota".</p>
                <div class="code-block">
# Di dalam main.py (Tower)
kapten_node = RaidNode(kapten_obj, "Kapten")

for h_id in id_anggota[1:]:
    anggota_obj = barrack_aktif[h_id]
    anggota_node = RaidNode(anggota_obj, "Anggota")
    
    # Menambahkan node anak ke node kapten
    kapten_node.tambah_unit(anggota_node) 
    
master_node.tambah_unit(kapten_node)
                </div>
            </div>

            <!-- Tab Content: Hash & Queue -->
            <div id="Hash" class="tab-content">
                <h3>Database & Antrean (Hash Table & Queue)</h3>
                <p><b>Hash Table:</b> Menyimpan seluruh rincian status pahlawan (*Blueprints*) sehingga pencariannya berkecepatan instan O(1).<br><b>Queue:</b> Menampung hero hasil gacha secara urut dengan metode FIFO (*First In First Out*).</p>
                <div class="code-block">
# Hash Table untuk Database Pahlawan Instan
Daftar_Hero = HashTable(400)
Daftar_Hero.tambah(hero_id, hero_info)
pencarian = Daftar_Hero.cari("H005")

# Queue untuk Antrean Gacha
antrean_gacha = Queue()
antrean_gacha.enqueue(hero_baru)   # Masuk ke belakang antrean
hero_diklaim = antrean_gacha.dequeue() # Keluar dari depan antrean
                </div>
            </div>

        </div>
    </section>

    <footer>
        <div class="container">
            <p>Dibangun oleh Kelompok 1 TI-B | Proyek Akhir Algoritma dan Struktur Data</p>
            <p style="margin-top: 0.5rem; font-size: 0.9rem; color: #64748b;">Menghidupkan barisan kode menjadi dunia petualangan tanpa batas.</p>
        </div>
    </footer>

    <script>
        // Tab switching logic
        function openTab(evt, tabName) {
            // Sembunyikan semua konten tab
            let tabContents = document.getElementsByClassName("tab-content");
            for (let i = 0; i < tabContents.length; i++) {
                tabContents[i].classList.remove("active");
            }

            // Hapus kelas aktif dari semua tombol
            let tabButtons = document.getElementsByClassName("tab-btn");
            for (let i = 0; i < tabButtons.length; i++) {
                tabButtons[i].classList.remove("active");
            }

            // Tampilkan tab yang diklik dan tandai tombolnya aktif
            document.getElementById(tabName).classList.add("active");
            evt.currentTarget.classList.add("active");
        }

        // Scroll Animation Observer
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, {
            threshold: 0.1
        });

        document.querySelectorAll('section').forEach(section => {
            observer.observe(section);
        });
    </script>
</body>
</html>
