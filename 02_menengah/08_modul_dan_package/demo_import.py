"""
================================================================================
MODUL 02: TINGKAT MENENGAH (INTERMEDIATE PYTHON)
FILE 08: Demonstrasi Sistem Modul, Package & Import Python
================================================================================
Tujuan Pembelajaran:
1. Memahami perbedaan Script vs Module vs Package.
2. Peran __init__.py dan penentuan antarmuka publik via __all__.
3. Cara kerja sys.path dan resolusi import di Python.
================================================================================
"""

import sys
from pathlib import Path

# Menambahkan direktori induk ke sys.path untuk memastikan import berjalan lancar
DIREKTORI_INI = Path(__file__).resolve().parent
if str(DIREKTORI_INI) not in sys.path:
    sys.path.insert(0, str(DIREKTORI_INI))

# Mengimpor modul dari package paket_matematika
from paket_matematika import (
    tambah,
    pangkat,
    hitung_rata_rata,
    hitung_median,
    hitung_standar_deviasi,
    VERSI_PAKET,
)

print("=" * 70)
print(f"📦 Berhasil Memuat 'paket_matematika' versi {VERSI_PAKET}")
print("=" * 70)

# Uji fungsi aritmatika
a, b = 12.5, 4.0
print(f"Hasil Tambah ({a} + {b}) = {tambah(a, b)}")
print(f"Hasil Pangkat ({a} ^ 2)   = {pangkat(a, 2)}")

# Uji fungsi statistik
skor_sampel = [80.0, 95.0, 75.0, 90.0, 85.0, 100.0]
print(f"\nData Sampel Nilai: {skor_sampel}")
print(f"Mean (Rata-rata) : {hitung_rata_rata(skor_sampel):.2f}")
print(f"Median           : {hitung_median(skor_sampel):.2f}")
print(f"Standar Deviasi  : {hitung_standar_deviasi(skor_sampel):.2f}")

print("\n" + "=" * 70)
print("✅ Modul dan package berhasil terintegrasi dengan baik!")
print("=" * 70)
