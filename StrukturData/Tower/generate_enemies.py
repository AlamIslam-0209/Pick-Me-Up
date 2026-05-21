import json

themes = {
    "Hutan Pemula": ["M01|Slime Rumput", "M02|Serigala", "M03|Goblin"],
    "Gua Lembap": ["M04|Kelelawar", "M05|Slime Racun", "M06|Laba-laba", "M07|Kadal Gua"],
    "Padang Rumput Angin": ["M08|Harpy", "M09|Serigala Angin", "M10|Goblin Pengintai"],
    "Reruntuhan Kuno": ["M11|Golem Batu", "M12|Tengkorak", "M13|Hantu Reruntuhan"],
    "Kastil Terbengkalai": ["M14|Ksatria Hantu", "M15|Gargoyle", "M16|Banshee"],
    "Gurun Pasir Panas": ["M17|Kalajengking Raksasa", "M18|Mummy", "M19|Cacing Pasir"],
    "Oasis Tersembunyi": ["M20|Kadal Air", "M21|Peri Penipu"],
    "Lembah Racun": ["M22|Bunga Beracun", "M23|Ular Kobra", "M24|Slime Miasma"],
    "Hutan Berbisik": ["M25|Treant", "M26|Roh Hutan"],
    "Pegunungan Es": ["M27|Yeti", "M28|Slime Es", "M29|Serigala Es"],
    "Kuil Beku": ["M28|Slime Es", "M29|Serigala Es", "M30|Ksatria Beku"],
    "Danau Kaca": ["M31|Naga Air Kecil", "M32|Slime Kaca"],
    "Gunung Berapi": ["M33|Golem Api", "M34|Kelelawar Api", "M35|Elemental Api"],
    "Lautan Lahar": ["M35|Elemental Api", "M36|Salamander Api", "M37|Iblis Lahar"],
    "Gua Kristal": ["M38|Golem Kristal", "M39|Laba-laba Kristal", "M40|Kelelawar Kristal"],
    "Jembatan Langit": ["M41|Harpy Elit", "M42|Griffin"],
    "Pulau Terapung": ["M43|Elemental Angin", "M44|Naga Angin"],
    "Dimensi Kesengsaraan": ["M45|Iblis Bayangan", "M46|Reaper", "M47|Gargoyle Hitam"],
    "Kuil Bintang": ["M48|Elemental Cahaya", "M49|Golem Bintang"],
    "Istana Langit": ["M50|Valkyrie", "M51|Malaikat Jatuh", "M52|Penjaga Gerbang Langit"]
}

bosses = [
    "Raja Slime Raksasa", "Ratu Laba-laba Gua", "Raja Harpy Badai",
    "Jenderal Golem Kuno", "Arch-Knight Kematian", "Firaun Terkutuk",
    "Lord Kadal Air", "Matriark Bunga Beracun", "Treant Purba",
    "Alpha Yeti", "Raja Ksatria Beku", "Naga Air Dewasa",
    "Raja Golem Magma", "Lord Iblis Lahar", "Ratu Laba-laba Kristal",
    "Raja Griffin Langit", "Arch-Dragon Angin", "The Grim Reaper",
    "Lord Golem Bintang", "Archangel of Ruin"
]

enemies = []
theme_idx = 0

for theme, monsters in themes.items():
    progress = theme_idx / 19.0
    
    base_hp = int(50 + (25000 - 50) * (progress ** 2))
    base_atk = int(15 + (1000 - 15) * (progress ** 2))
    
    for m in monsters:
        mid, mname = m.split("|")
        if not any(e["id"] == mid for e in enemies):
            hp_variation = int(base_hp * (0.9 + 0.2 * (len(enemies) % 3)))
            atk_variation = int(base_atk * (0.9 + 0.2 * (len(enemies) % 3)))
            enemies.append({
                "id": mid,
                "name": mname,
                "hp": hp_variation,
                "atk": atk_variation,
                "is_boss": False
            })
    
    boss_hp = int(500 + (150000 - 500) * (progress ** 2))
    boss_atk = int(150 + (3500 - 150) * (progress ** 2))
    
    enemies.append({
        "id": f"BOSS_{theme_idx + 1:02d}",
        "name": bosses[theme_idx],
        "hp": boss_hp,
        "atk": boss_atk,
        "is_boss": True
    })
    
    theme_idx += 1

with open("/home/alam/Coding/Game/Pick-Me-Up/data/blueprint_enemy.json", "w") as f:
    json.dump(enemies, f, indent=4)
print(f"Generated {len(enemies)} enemies.")
