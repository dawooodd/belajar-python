"""
================================================================================
MODUL 01: DASAR PEMROGRAMAN PYTHON
FILE 01: Sintaksis Dasar, Variabel, Tipe Data & Modern Type Hinting
================================================================================
Tujuan Pembelajaran:
1. Memahami filosofi sintaks Python, indentasi, dan kaidah PEP 8.
2. Mengenal variabel dinamis vs referensi memori (id(), is vs ==).
3. Menguasai tipe data primitif bawaan (int, float, complex, bool, str, NoneType).
4. Menerapkan Modern Type Hinting (Python 3.10+ PEP 604: int | str, list[int], dll).
5. Teknik manipulasi string tingkat lanjut dan f-string debugging (f"{var=}").
================================================================================
"""

from __future__ import annotations  # Memungkinkan type hint modern dievaluasi secara lazily
import sys
from typing import Final, Any

# ------------------------------------------------------------------------------
# 1. Filosofi dan Konvensi PEP 8
# ------------------------------------------------------------------------------
# Konstanta ditulis dalam UPPER_CASE (secara konvensi dan typing.Final)
NAMA_APLIKASI: Final[str] = "BelajarPythonMastery"
VERSI_SISTEM: Final[str] = "2026.10"

print("=" * 70)
print(f"🚀 Selamat Datang di {NAMA_APLIKASI} - Versi {VERSI_SISTEM}")
print(f"📌 Berjalan pada Python: {sys.version.split()[0]} ({sys.platform})")
print("=" * 70)


# ------------------------------------------------------------------------------
# 2. Variabel & Sistem Dynamic Typing
# ------------------------------------------------------------------------------
# Python menggunakan dynamic typing: tipe variabel ditentukan saat runtime.
# Namun, sejak Python 3.5+ dan disempurnakan di Python 3.10+, sangat direkomendasikan
# menggunakan Type Annotations untuk maintainability & static analyzer (mypy).

umur_pengguna: int = 25
tinggi_badan_cm: float = 175.5
apakah_aktif: bool = True
catatan_khusus: str | None = None  # Union syntax modern (PEP 604) setara Optional[str]

print("\n--- [1] Variabel & Dynamic Typing ---")
print(f"Umur: {umur_pengguna} (Tipe: {type(umur_pengguna).__name__})")
print(f"Tinggi: {tinggi_badan_cm} cm (Tipe: {type(tinggi_badan_cm).__name__})")
print(f"Status Aktif: {apakah_aktif} (Tipe: {type(apakah_aktif).__name__})")
print(f"Catatan: {catatan_khusus} (Tipe: {type(catatan_khusus).__name__})")


# ------------------------------------------------------------------------------
# 3. Referensi Memori: '==' vs 'is' & Fungsi id()
# ------------------------------------------------------------------------------
# '==' membandingkan VALUE / NILAI dari objek
# 'is' membandingkan IDENTITY / ALAMAT MEMORI objek (apakah objek yang sama persis)

print("\n--- [2] Memori & Perbedaan '==' vs 'is' ---")
daftar_a: list[int] = [1, 2, 3]
daftar_b: list[int] = [1, 2, 3]
daftar_c: list[int] = daftar_a

print(f"daftar_a ID: {id(daftar_a)}")
print(f"daftar_b ID: {id(daftar_b)}")
print(f"daftar_c ID: {id(daftar_c)}")

print(f"daftar_a == daftar_b : {daftar_a == daftar_b}  (Nilainya sama)")
print(f"daftar_a is daftar_b : {daftar_a is daftar_b}  (Beda alamat memori)")
print(f"daftar_a is daftar_c : {daftar_a is daftar_c}  (Objek memori yang sama)")

# Integers caching (Integer Interning pada rentang -5 s/d 256)
x: int = 100
y: int = 100
print(f"Integer interning x is y (100): {x is y}")


# ------------------------------------------------------------------------------
# 4. Tipe Data Bilangan (Numeric Types)
# ------------------------------------------------------------------------------
print("\n--- [3] Tipe Data Bilangan ---")
bilangan_bulat: int = 1_000_000_000  # Underscore readability (PEP 515)
bilangan_desimal: float = 3.141592653589793
bilangan_kompleks: complex = 3 + 4j

print(f"Bilangan besar (readable): {bilangan_bulat:,}")
print(f"Bilangan kompleks: {bilangan_kompleks}, Real: {bilangan_kompleks.real}, Imag: {bilangan_kompleks.imag}")
print(f"Absolute kompleks (magnitudo): {abs(bilangan_kompleks)}")


# ------------------------------------------------------------------------------
# 5. Nilai Kebenaran (Truthy & Falsy)
# ------------------------------------------------------------------------------
# Objek yang bernilai FALSY:
# - None, False
# - Angka nol: 0, 0.0, 0j
# - Kumpulan kosong: '', (), [], {}, set(), range(0)
# Semua objek selain di atas adalah TRUTHY!

print("\n--- [4] Aturan Truthy & Falsy ---")
nilai_evaluasi: list[Any] = [0, 1, "", "Halo", [], [1, 2], None, {}, {"kunci": "nilai"}]

for nilai in nilai_evaluasi:
    status_boolean = bool(nilai)
    print(f"Nilai: {repr(nilai):<15} -> Boolean: {str(status_boolean):<6} ({'TRUTHY' if status_boolean else 'FALSY'})")


# ------------------------------------------------------------------------------
# 6. Fitur Canggih String & f-Strings Modern
# ------------------------------------------------------------------------------
print("\n--- [5] String Formatting Tingkat Lanjut (f-strings) ---")
produk: str = "Laptop Pro Max"
harga: float = 18999900.5
diskon: float = 0.125  # 12.5%

# Format specifiers
# :>20 = Rata kanan selebar 20 karakter
# :<20 = Rata kiri
# :^20 = Rata tengah
# :,.2f = Pemisah ribuan koma dengan 2 desimal
# :.1% = Format persentase

print(f"Produk     : {produk:<25}")
print(f"Harga Asli : Rp {harga:>15,.2f}")
print(f"Diskon     : {diskon:>15.1%}")
print(f"Total Bayar: Rp {(harga * (1 - diskon)):>15,.2f}")

# Debugging dengan f-string (Syntax var= diperkenalkan sejak Python 3.8)
lebar = 10
panjang = 25
luas = panjang * lebar
print(f"\n[Debug Mode Otomatis] {panjang=}, {lebar=}, {luas=}")


# ------------------------------------------------------------------------------
# 7. Ringkasan & Best Practice Checklist
# ------------------------------------------------------------------------------
print("\n" + "=" * 70)
print("✅ KESIMPULAN & BEST PRACTICE FILE 01:")
print("1. Gunakan 'snake_case' untuk variabel dan fungsi.")
print("2. Gunakan 'UPPER_CASE' untuk konstanta.")
print("3. Selalu sertakan type hints modern (contoh: int | str, bukan Union[int, str]).")
print("4. Gunakan 'is' hanya saat membandingkan dengan None atau singleton (contoh: if x is None:).")
print("5. Manfaatkan f-string `{var=}` saat debugging cepat.")
print("=" * 70)

if __name__ == "__main__":
    print("Modul 01 dieksekusi langsung secara sukses.")
