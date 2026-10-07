"""
================================================================================
MODUL 01: DASAR PEMROGRAMAN PYTHON
FILE 05: Struktur Data Bawaan, Comprehensions & Modul Collections
================================================================================
Tujuan Pembelajaran:
1. Memahami 4 pilar struktur data: List, Tuple, Set, dan Dictionary.
2. Membedakan Mutabilitas vs Immutabilitas serta Shallow Copy vs Deep Copy.
3. Menguasai Slicing, Extended Unpacking (*rest), dan Operator Penggabungan Dict (|).
4. Menulis Comprehensions tingkat lanjut (List, Set, Dict).
5. Memanfaatkan modul bawaan collections (Counter, defaultdict, deque, namedtuple).
================================================================================
"""

import copy
from collections import Counter, defaultdict, deque, namedtuple

print("=" * 70)
print("--- [1] List: Mutabilitas, Slicing & Copying ---")

angka: list[int] = [10, 20, 30, 40, 50, 60, 70, 80, 90]

# Slicing: [start:stop:step]
print(f"Original       : {angka}")
print(f"Ambil 3 pertama: {angka[:3]}")
print(f"Ambil 3 terakhir: {angka[-3:]}")
print(f"Langkah 2 (step): {angka[::2]}")
print(f"Balik list      : {angka[::-1]}")

# Shallow Copy vs Deep Copy
data_asli = [[1, 2], [3, 4]]
shallow_copy = list(data_asli)       # atau data_asli.copy()
deep_copy = copy.deepcopy(data_asli)

data_asli[0][0] = 999
print(f"\nEfek modifikasi nested list pada shallow copy: {shallow_copy} (Terpengaruh!)")
print(f"Efek modifikasi nested list pada deep copy   : {deep_copy} (Tetap aman)")


# ------------------------------------------------------------------------------
# 2. Tuple & Extended Unpacking (Pattern Matching Sederhana)
# ------------------------------------------------------------------------------
print("\n--- [2] Tuple & Extended Unpacking ---")
# Tuple bersifat IMMUTABLE (tidak dapat diubah setelah dibuat), sangat hemat memori.

titik_gps = (-6.2088, 106.8456)
lat, lon = titik_gps
print(f"Latitude: {lat}, Longitude: {lon}")

# Extended Unpacking (*operator)
skor_siswa = [95, 80, 85, 70, 90, 100]
skor_urut = sorted(skor_siswa)
terendah, *nilai_tengah, tertinggi = skor_urut
print(f"Nilai Terendah : {terendah}")
print(f"Nilai Tengah   : {nilai_tengah}")
print(f"Nilai Tertinggi: {tertinggi}")


# ------------------------------------------------------------------------------
# 3. Set: Kecepatan O(1) & Operasi Himpunan Matematika
# ------------------------------------------------------------------------------
print("\n--- [3] Set & Operasi Himpunan Matematika ---")
# Set bersifat unik, tidak berurutan, dan pencarian 'x in s' memiliki kompleksitas O(1)

skill_backend = {"Python", "PostgreSQL", "Docker", "Redis"}
skill_frontend = {"JavaScript", "TypeScript", "React", "Docker"}

print(f"Union / Gabungan (|)               : {skill_backend | skill_frontend}")
print(f"Intersection / Irisan (&)           : {skill_backend & skill_frontend}")
print(f"Difference / Hanya di Backend (-)   : {skill_backend - skill_frontend}")
print(f"Symmetric Difference / Non-irisan (^): {skill_backend ^ skill_frontend}")


# ------------------------------------------------------------------------------
# 4. Dictionary: Fitur Modern & Operator Merge (|)
# ------------------------------------------------------------------------------
print("\n--- [4] Dictionary & Operator Merge Modern (Python 3.9+) ---")
config_default = {"host": "localhost", "port": 8000, "debug": True}
config_env = {"port": 5000, "workers": 4}

# Operator Merge (|) dan Update (|=)
config_final = config_default | config_env
print(f"Konfigurasi Akhir (Merged): {config_final}")

# Mengambil nilai secara aman dengan .get()
port = config_final.get("timeout", 30)  # 30 adalah default value jika key tidak ada
print(f"Port / Timeout: {port}")


# ------------------------------------------------------------------------------
# 5. Comprehensions Tingkat Lanjut (List, Dict, Set)
# ------------------------------------------------------------------------------
print("\n--- [5] Comprehensions Bersarang & Efisien ---")

# 1. List Comprehension dengan filter
daftar_kata = ["python", "django", "fastapi", "ai", "machine learning"]
kata_panjang = [kata.upper() for kata in daftar_kata if len(kata) > 5]
print(f"Kata > 5 huruf (Upper): {kata_panjang}")

# 2. Dict Comprehension
mahasiswa = [("Andi", 85), ("Bella", 92), ("Citra", 78)]
grade_dict = {
    nama: "A" if nilai >= 90 else "B" if nilai >= 80 else "C"
    for nama, nilai in mahasiswa
}
print(f"Dict Comprehension: {grade_dict}")

# 3. Set Comprehension
panjang_karakter_unik = {len(k) for k in daftar_kata}
print(f"Set Comprehension (Panjang unik): {panjang_karakter_unik}")

# 4. Flatten Matrix 2D menggunakan nested list comprehension
matriks = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [elemen for baris in matriks for elemen in baris]
print(f"Matriks Flattened: {flattened}")


# ------------------------------------------------------------------------------
# 6. Modul Standar: collections
# ------------------------------------------------------------------------------
print("\n--- [6] Modul collections Bawaan Python ---")

# A. Counter (Menghitung frekuensi item secara instan)
kalimat = "python adalah bahasa pemrograman yang mudah dan python sangat populer"
kata_counter = Counter(kalimat.split())
print(f"Top 2 Kata terbanyak: {kata_counter.most_common(2)}")

# B. defaultdict (Mencegah KeyError saat append / count)
grup_kategori = defaultdict(list)
produk_list = [("Elektronik", "HP"), ("Pakaian", "Kemeja"), ("Elektronik", "Laptop")]
for kategori, item in produk_list:
    grup_kategori[kategori].append(item)
print(f"defaultdict hasil pengelompokan: {dict(grup_kategori)}")

# C. deque (Double-ended queue dengan O(1) append dan pop dari kedua ujung)
antrean = deque(["Pengguna 1", "Pengguna 2"])
antrean.append("Pengguna 3")       # Tambah kanan
antrean.appendleft("VIP Pengguna") # Tambah kiri secara O(1)
print(f"Antrean deque: {antrean}")
dilayani = antrean.popleft()
print(f"Dilayani duluan: {dilayani}, Sisa: {antrean}")

# D. namedtuple (Objek tuple ringan dengan atribut yang terbaca)
Pengguna = namedtuple("Pengguna", ["id", "nama", "email"])
u1 = Pengguna(id=1, nama="Rian", email="rian@example.com")
print(f"namedtuple: ID={u1.id}, Nama={u1.nama}, Email={u1.email}")


print("\n" + "=" * 70)
print("✅ KESIMPULAN & BEST PRACTICE FILE 05:")
print("1. Gunakan tuple untuk data tetap (immutable) karena lebih hemat memori dan hashable.")
print("2. Gunakan set untuk operasi keanggotaan (membership test 'in') berkecepatan O(1).")
print("3. Gunakan operator dict union `|` untuk menggabungkan konfigurasi.")
print("4. Gunakan `deque` jika membutuhkan struktur data antrean FIFO (hindari `list.pop(0)` berkecepatan O(n)).")
print("5. Gunakan `defaultdict` dan `Counter` untuk menyederhanakan kode pengelompokan.")
print("=" * 70)
