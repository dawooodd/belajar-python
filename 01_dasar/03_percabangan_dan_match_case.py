"""
================================================================================
MODUL 01: DASAR PEMROGRAMAN PYTHON
FILE 03: Alur Kontrol, Percabangan & Structural Pattern Matching (match-case)
================================================================================
Tujuan Pembelajaran:
1. Menguasai percabangan if-elif-else dan Ternary Operator.
2. Menerapkan pola Guard Clause / Early Return demi kode yang clean.
3. Menguasai Structural Pattern Matching (match-case) Python 3.10+:
   - Literal Pattern & Wildcard (_)
   - Sequence Pattern (Destructuring list/tuple)
   - Mapping Pattern (Destructuring dictionary)
   - Class/Object Pattern
   - Guard Condition (if di dalam case)
================================================================================
"""

from dataclasses import dataclass
from typing import Any

print("=" * 70)
print("--- [1] If-Elif-Else & Ternary Operator ---")

skor: int = 87

# If-Elif-Else Tradisional
if skor >= 90:
    grade = "A (Cumlaude)"
elif skor >= 80:
    grade = "B (Sangat Baik)"
elif skor >= 70:
    grade = "C (Cukup)"
else:
    grade = "D (Remedial)"

print(f"Skor: {skor} -> Grade: {grade}")

# Ternary Operator: <nilai_jika_true> if <kondisi> else <nilai_jika_false>
status_kelulusan = "LULUS" if skor >= 75 else "TIDAK LULUS"
print(f"Status Kelulusan: {status_kelulusan}")


# ------------------------------------------------------------------------------
# 2. Guard Clause / Early Return Pattern
# ------------------------------------------------------------------------------
print("\n--- [2] Clean Code Pattern: Guard Clause ---")
# Menghindari deep nesting (sarang burung / arrow anti-pattern)

def proses_transaksi(saldo: float, jumlah_tarik: float, akun_aktif: bool) -> str:
    # ❌ BAD PRACTICE:
    # if akun_aktif:
    #     if jumlah_tarik > 0:
    #         if saldo >= jumlah_tarik:
    #             return "Sukses"
    
    # ✅ BEST PRACTICE (Guard Clauses):
    if not akun_aktif:
        return "Gagal: Akun sedang dibekukan."
    if jumlah_tarik <= 0:
        return "Gagal: Jumlah penarikan harus lebih dari 0."
    if saldo < jumlah_tarik:
        return "Gagal: Saldo tidak mencukupi."
    
    saldo_baru = saldo - jumlah_tarik
    return f"Sukses! Sisa saldo: Rp {saldo_baru:,.2f}"

print(proses_transaksi(1_000_000, 250_000, True))
print(proses_transaksi(100_000, 200_000, True))
print(proses_transaksi(1_000_000, 50_000, False))


# ------------------------------------------------------------------------------
# 3. Structural Pattern Matching (match - case) - Python 3.10+
# ------------------------------------------------------------------------------
# match-case bukan sekadar 'switch-case' bahasa C/Java, melainkan destrukturisasi data yang canggih!

print("\n--- [3] Match-Case: HTTP Status & OR Pattern ---")

def tangani_status_http(status_code: int) -> str:
    match status_code:
        case 200 | 201:
            return "2xx: Sukses (OK / Created)"
        case 301 | 302:
            return "3xx: Redirection"
        case 400:
            return "400: Bad Request - Periksa input payload"
        case 401 | 403:
            return "4xx: Unauthorized atau Forbidden"
        case 404:
            return "404: Not Found - Resource tidak ditemukan"
        case 500 | 502 | 503:
            return "5xx: Server Error"
        case _:
            return f"Status {status_code} tidak dikenal."

for code in [200, 404, 500, 999]:
    print(f"HTTP {code} -> {tangani_status_http(code)}")


print("\n--- [4] Match-Case: Sequence Pattern & Destructuring ---")

def proses_perintah(command: list[str]) -> str:
    match command:
        case ["keluar"]:
            return "Menutup aplikasi..."
        case ["buat", nama_file]:
            return f"Membuat file baru: '{nama_file}'"
        case ["salin", sumber, tujuan]:
            return f"Menyalin dari '{sumber}' ke '{tujuan}'"
        case ["hapus", *daftar_file]:  # Menerima sisa argumen sebagai list
            return f"Menghapus beberapa file: {daftar_file}"
        case _:
            return f"Perintah '{' '.join(command)}' tidak valid!"

print(proses_perintah(["buat", "skrip.py"]))
print(proses_perintah(["salin", "data.csv", "backup.csv"]))
print(proses_perintah(["hapus", "temp1.log", "temp2.log", "cache.bin"]))
print(proses_perintah(["format", "c:"]))


print("\n--- [5] Match-Case: Mapping Pattern (JSON/Dict) & Guards ---")

def proses_payload_api(payload: dict[str, Any]) -> str:
    match payload:
        case {"aksi": "pesan", "jumlah": int(jml), "pembayaran": "lunas"} if jml > 100:
            return f"Pesanan grosir ({jml} item) telah lunas! Beri diskon khusus."
        case {"aksi": "pesan", "jumlah": int(jml), "pembayaran": "lunas"}:
            return f"Pesanan reguler ({jml} item) berhasil diproses."
        case {"aksi": "pesan", "pembayaran": "pending"}:
            return "Pesanan diterima, menunggu konfirmasi pembayaran."
        case {"aksi": "batal", "alasan": str(alasan)}:
            return f"Pembatalan pesanan dicatat. Alasan: {alasan}"
        case _:
            return "Payload format tidak valid."

print(proses_payload_api({"aksi": "pesan", "jumlah": 150, "pembayaran": "lunas"}))
print(proses_payload_api({"aksi": "pesan", "jumlah": 5, "pembayaran": "lunas"}))
print(proses_payload_api({"aksi": "batal", "alasan": "Ingin ganti alamat"}))


print("\n--- [6] Match-Case: Class/Object Pattern Matching ---")

@dataclass
class Titik:
    x: float
    y: float

def klasifikasi_posisi(t: Titik) -> str:
    match t:
        case Titik(x=0, y=0):
            return "Titik berada tepat di Titik Pusat (Origin)"
        case Titik(x=0, y=y):
            return f"Titik berada di Sumbu Y pada y={y}"
        case Titik(x=x, y=0):
            return f"Titik berada di Sumbu X pada x={x}"
        case Titik(x=x, y=y) if x == y:
            return f"Titik berada di garis diagonal simetris ({x}, {y})"
        case Titik(x=x, y=y):
            return f"Titik umum di koordinat ({x}, {y})"

print(klasifikasi_posisi(Titik(0, 0)))
print(klasifikasi_posisi(Titik(0, 15)))
print(klasifikasi_posisi(Titik(7, 7)))
print(klasifikasi_posisi(Titik(12, -4)))


print("\n" + "=" * 70)
print("✅ KESIMPULAN & BEST PRACTICE FILE 03:")
print("1. Gunakan Guard Clause untuk mereduksi level indentasi bersarang.")
print("2. Gunakan ternary hanya untuk ekspresi sederhana satu baris.")
print("3. Gunakan 'match-case' saat perlu mendestrukturisasi list, tuple, dict, atau objek.")
print("4. Tambahkan 'case _:' sebagai default fallback untuk menghindari unhandled state.")
print("=" * 70)
