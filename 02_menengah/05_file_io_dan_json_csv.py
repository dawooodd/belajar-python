"""
================================================================================
MODUL 02: TINGKAT MENENGAH (INTERMEDIATE PYTHON)
FILE 05: Modern File I/O dengan pathlib, Pemrosesan CSV & JSON Serializer
================================================================================
Tujuan Pembelajaran:
1. Menggunakan pathlib.Path untuk manipulasi berkas lintas platform (Windows/Linux/Mac).
2. Pentingnya penanganan encoding eksplisit (encoding='utf-8').
3. Membaca dan menulis CSV menggunakan csv.DictReader dan csv.DictWriter.
4. Serialisasi JSON dan penanganan tipe data non-standar (datetime, UUID) via Custom Encoder.
5. Operasi berkas biner (binary read/write).
================================================================================
"""

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any

print("=" * 70)
print("--- [1] Modern File I/O dengan pathlib.Path ---")

# Menentukan direktori kerja secara dinamis dan aman
DIR_KERJA = Path(__file__).resolve().parent / "data_output"
DIR_KERJA.mkdir(parents=True, exist_ok=True)

file_teks = DIR_KERJA / "catatan.txt"

# Menulis teks (write_text praktis untuk file kecil)
file_teks.write_text("Belajar Python Modern 2026\nKompilasi Modul Terlengkap.", encoding="utf-8")

# Membaca teks (read_text)
isi_teks = file_teks.read_text(encoding="utf-8")
print(f"Path Berkas : {file_teks}")
print(f"Ukuran File : {file_teks.stat().st_size} bytes")
print(f"Isi Berkas  :\n{isi_teks}")


# ------------------------------------------------------------------------------
# 2. Pemrosesan Berkas CSV dengan csv.DictWriter & csv.DictReader
# ------------------------------------------------------------------------------
print("\n--- [2] Pemrosesan CSV (DictWriter & DictReader) ---")

file_csv = DIR_KERJA / "karyawan.csv"

data_karyawan = [
    {"nik": "EMP001", "nama": "Ahmad Fauzi", "divisi": "Engineering", "gaji": 15000000},
    {"nik": "EMP002", "nama": "Dewi Sartika", "divisi": "Data Science", "gaji": 18000000},
    {"nik": "EMP003", "nama": "Rian Kusuma", "divisi": "Product", "gaji": 14000000},
]

# Menulis ke file CSV
header = ["nik", "nama", "divisi", "gaji"]
with open(file_csv, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=header)
    writer.writeheader()
    writer.writerows(data_karyawan)

print(f"✅ Berhasil menulis CSV ke {file_csv.name}")

# Membaca kembali dari CSV
print("\nMembaca data dari CSV:")
with open(file_csv, mode="r", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"- {row['nama']} ({row['divisi']}): Rp {int(row['gaji']):,}")


# ------------------------------------------------------------------------------
# 3. Pemrosesan JSON & Custom Encoder untuk Objek Kompleks
# ------------------------------------------------------------------------------
print("\n--- [3] JSON Serializer & Custom JSON Encoder ---")

file_json = DIR_KERJA / "laporan.json"

class ModelLaporan:
    def __init__(self, judul: str, nominal: float) -> None:
        self.judul = judul
        self.nominal = nominal
        self.waktu = datetime.now()

class CustomJSONEncoder(json.JSONEncoder):
    """Menangani serialisasi tipe data bawaan Python yang tidak didukung JSON murni."""
    def default(self, obj: Any) -> Any:
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, ModelLaporan):
            return {"judul": obj.judul, "nominal": obj.nominal, "waktu": obj.waktu}
        if isinstance(obj, Path):
            return str(obj)
        return super().default(obj)

laporan_obj = ModelLaporan("Laporan Penjualan Q1", 450_000_000.0)

payload = {
    "status": "APPROVED",
    "kode_transaksi": "TRX-2026-99",
    "data": laporan_obj,
    "path_arsip": file_json
}

# Simpan ke file JSON
with open(file_json, mode="w", encoding="utf-8") as f:
    json.dump(payload, f, indent=2, cls=CustomJSONEncoder)

print(f"✅ JSON berhasil diserialisasi dan disimpan ke: {file_json.name}")

# Baca kembali JSON
with open(file_json, mode="r", encoding="utf-8") as f:
    data_terbaca = json.load(f)
    print("Isi JSON Terbaca:")
    print(json.dumps(data_terbaca, indent=2))


# ------------------------------------------------------------------------------
# 4. Operasi Biner (Binary I/O)
# ------------------------------------------------------------------------------
print("\n--- [4] Binary Read/Write (Bytes) ---")

file_biner = DIR_KERJA / "data.bin"

# Menulis representasi bytes
data_byte = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"
file_biner.write_bytes(data_byte)

# Membaca bytes
byte_terbaca = file_biner.read_bytes()
print(f"Header biner terbaca: {byte_terbaca[:8]}")


print("\n" + "=" * 70)
print("✅ KESIMPULAN & BEST PRACTICE FILE 05:")
print("1. Tinggalkan `os.path` lama — selalu gunakan modul modern `pathlib.Path`.")
print("2. Selalu tulis `encoding='utf-8'` secara eksplisit saat membuka file teks.")
print("3. Selalu tambahkan `newline=''` pada open() saat menangani file CSV di Windows.")
print("4. Buat subkelas `json.JSONEncoder` untuk objek kustom (datetime, UUID, Enum).")
print("=" * 70)
