"""
================================================================================
MODUL 01: DASAR PEMROGRAMAN PYTHON
FILE 06: Fungsi, Scope LEGB, Lambda & Functional Programming Paradigms
================================================================================
Tujuan Pembelajaran:
1. Memahami anatomi fungsi, Positional-Only (/), dan Keyword-Only (*) arguments.
2. Membongkar jebakan umum: The Mutable Default Argument Bug (def func(items=[]))!
3. Penguasaan *args dan **kwargs secara mendalam.
4. Memahami Scope Variabel dengan aturan LEGB (Local, Enclosing, Global, Built-in).
5. Lambda functions dan Higher-Order Functions (map, filter, reduce, sorted key).
================================================================================
"""

from functools import reduce
from typing import Callable, Any

print("=" * 70)
print("--- [1] Positional-Only (/) dan Keyword-Only (*) Parameters ---")
# Sintaks Python 3.8+ (PEP 570):
# Sebelum '/'  -> Wajib dipanggil sebagai Positional
# Setelah '*'   -> Wajib dipanggil sebagai Keyword

def buat_profil_pengguna(
    user_id: int,           # Sebelum /: Harus Positional
    /,
    nama: str,              # Antara / dan *: Bebas (Positional atau Keyword)
    *,
    email: str,             # Setelah *: Wajib Keyword
    role: str = "member"    # Wajib Keyword dengan default
) -> dict[str, Any]:
    """Membuat profil pengguna dengan validasi argumen ketat."""
    return {
        "id": user_id,
        "nama": nama,
        "email": email,
        "role": role
    }

# Pemanggilan yang valid:
profil_1 = buat_profil_pengguna(101, "Bayu", email="bayu@perusahaan.com", role="admin")
profil_2 = buat_profil_pengguna(102, nama="Siti", email="siti@perusahaan.com")
print(f"Profil 1: {profil_1}")
print(f"Profil 2: {profil_2}")

# Contoh pemanggilan yang SALAH (akan melempar TypeError jika di-uncomment):
# buat_profil_pengguna(user_id=103, "Riko", email="riko@mail.com") # ❌ TypeError: user_id positional-only!
# buat_profil_pengguna(104, "Doni", "doni@mail.com")              # ❌ TypeError: email keyword-only!


# ------------------------------------------------------------------------------
# 2. Jebakan Mutable Default Argument (The Infamous Bug)
# ------------------------------------------------------------------------------
print("\n--- [2] Jebakan Mutable Default Argument & Solusinya ---")

# ❌ BAD PRACTICE (JANGAN LAKUKAN INI):
def tambah_tugas_buruk(tugas: str, daftar_tugas: list[str] = []) -> list[str]:
    # Default list [] hanya dibuat SEKALI saat fungsi didefinisikan di memori!
    daftar_tugas.append(tugas)
    return daftar_tugas

print("Efek Buruk:")
print("Pemanggilan 1:", tambah_tugas_buruk("Belajar Python"))
print("Pemanggilan 2:", tambah_tugas_buruk("Buat API")) # Bug: 'Belajar Python' masih ada di list!

# ✅ BEST PRACTICE (Gunakan Sentinel None):
def tambah_tugas_benar(tugas: str, daftar_tugas: list[str] | None = None) -> list[str]:
    if daftar_tugas is None:
        daftar_tugas = []
    daftar_tugas.append(tugas)
    return daftar_tugas

print("\nEfek Benar:")
print("Pemanggilan 1:", tambah_tugas_benar("Belajar Python"))
print("Pemanggilan 2:", tambah_tugas_benar("Buat API")) # Bersih dan terisolasi!


# ------------------------------------------------------------------------------
# 3. Dynamic Arguments: *args dan **kwargs
# ------------------------------------------------------------------------------
print("\n--- [3] Fleksibilitas *args dan **kwargs ---")

def kalkulator_log(operasi: str, *angka: float, **metadata: str) -> None:
    """Menerima argumen jumlah bebas dan kwargs metadata opsional."""
    if operasi == "kali":
        hasil = 1
        for x in angka:
            hasil *= x
    elif operasi == "tambah":
        hasil = sum(angka)
    else:
        hasil = 0

    print(f"[{metadata.get('tag', 'INFO')}] Operasi '{operasi}' pada {angka} = {hasil}")
    if "user" in metadata:
        print(f"  -> Dieksekusi oleh: {metadata['user']}")

kalkulator_log("tambah", 10, 20, 30, 40, tag="MATH_RUN", user="Admin")
kalkulator_log("kali", 2, 3, 4, tag="MATH_MULT")


# ------------------------------------------------------------------------------
# 4. Scope Variabel: Aturan LEGB, global, dan nonlocal
# ------------------------------------------------------------------------------
print("\n--- [4] Scope Variabel & Keyword nonlocal ---")
# LEGB: Local -> Enclosing -> Global -> Built-in

penghitung_global = 0

def generator_counter():
    hitung_enclosing = 0  # Enclosing scope
    
    def increment():
        nonlocal hitung_enclosing  # Mengakses dan memutasi variabel di enclosing scope
        hitung_enclosing += 1
        return hitung_enclosing
    
    return increment

counter_a = generator_counter()
print(f"Counter A Panggilan 1: {counter_a()}")
print(f"Counter A Panggilan 2: {counter_a()}")
counter_b = generator_counter()
print(f"Counter B Panggilan 1: {counter_b()} (Terisolasi dari Counter A)")


# ------------------------------------------------------------------------------
# 5. Lambda Functions & Higher-Order Functions
# ------------------------------------------------------------------------------
print("\n--- [5] Functional Programming: map, filter, reduce & sorted ---")

daftar_angka = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# map(): Transformasi tiap elemen
kuadrat = list(map(lambda x: x**2, daftar_angka))
print(f"map() kuadrat: {kuadrat}")

# filter(): Memilih elemen yang memenuhi kondisi boolean
genap = list(filter(lambda x: x % 2 == 0, daftar_angka))
print(f"filter() genap: {genap}")

# reduce(): Akumulasi seluruh elemen menjadi satu nilai
total_perkalian = reduce(lambda acc, x: acc * x, [1, 2, 3, 4, 5])
print(f"reduce() faktorial 5: {total_perkalian}")

# Custom sorting dengan lambda key
inventori = [
    {"nama": "Monitor", "harga": 2500000, "stok": 12},
    {"nama": "Keyboard", "harga": 650000, "stok": 45},
    {"nama": "Mouse", "harga": 350000, "stok": 80},
    {"nama": "Headset", "harga": 1200000, "stok": 15},
]

# Urutkan berdasarkan harga termurah
urut_harga = sorted(inventori, key=lambda item: item["harga"])
print("\nProduk diurutkan berdasarkan harga termurah:")
for item in urut_harga:
    print(f"- {item['nama']:<10}: Rp {item['harga']:>10,}")


print("\n" + "=" * 70)
print("✅ KESIMPULAN & BEST PRACTICE FILE 06:")
print("1. Selalu gunakan `None` sebagai default argument untuk objek yang mutable (list/dict/set).")
print("2. Gunakan `/` dan `*` untuk mendesain API fungsi yang jelas dan tegas.")
print("3. Pahami aturan LEGB dan gunakan `nonlocal` saat membuat fungsi closure bersarang.")
print("4. Gunakan lambda hanya untuk ekspresi satu baris sederhana; jika rumit, buat `def` biasa.")
print("=" * 70)
