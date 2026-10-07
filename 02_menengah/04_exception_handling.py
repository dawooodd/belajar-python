"""
================================================================================
MODUL 02: TINGKAT MENENGAH (INTERMEDIATE PYTHON)
FILE 04: Penanganan Exception, Custom Exception, Exception Chaining & ExceptionGroup
================================================================================
Tujuan Pembelajaran:
1. Memahami alur kerja try, except, else, and finally.
2. Menghindari anti-pattern: Bare except and swallowing exceptions.
3. Merancang hierarki Custom Exception untuk sistem enterprise.
4. Menerapkan Exception Chaining (raise ... from ...).
5. Memahami ExceptionGroup dan sintaks except* (Python 3.11+).
================================================================================
"""

import sys
from contextlib import suppress

print("=" * 70)
print("--- [1] Siklus Lengkap: try - except - else - finally ---")

def baca_dan_hitung_rasio(angka_str: str, pembagi: float) -> float | None:
    try:
        angka = float(angka_str)
        hasil = angka / pembagi
    except ValueError as e:
        print(f"❌ Kesalahan Konversi: String '{angka_str}' bukan angka ({e})")
        return None
    except ZeroDivisionError as e:
        print(f"❌ Kesalahan Matematika: Tidak bisa membagi dengan nol ({e})")
        return None
    else:
        # 'else' hanya dieksekusi JIKA TIDAK ADA EXCEPTION SAMA SEKALI
        print("✅ Kalkulasi berhasil tanpa hambatan!")
        return hasil
    finally:
        # 'finally' SELALU dieksekusi apapun yang terjadi (pembersihan resource)
        print("🧹 [Cleanup] Blok finally selesai dieksekusi.")

print("Kasus Sukses:")
baca_dan_hitung_rasio("100", 4)

print("\nKasus Zero Division:")
baca_dan_hitung_rasio("100", 0)


# ------------------------------------------------------------------------------
# 2. Hierarki Custom Domain Exceptions
# ------------------------------------------------------------------------------
print("\n--- [2] Merancang Hierarki Custom Exceptions ---")

class AplikasiError(Exception):
    """Base exception untuk seluruh modul aplikasi kita."""
    pass

class DatabaseError(AplikasiError):
    """Exception terkait operasi database."""
    def __init__(self, pesan: str, kode_status: int = 500) -> None:
        super().__init__(pesan)
        self.kode_status = kode_status

class RecordNotFoundError(DatabaseError):
    """Dilempar saat entitas tidak ditemukan di database."""
    def __init__(self, entitas: str, id_entitas: int | str) -> None:
        super().__init__(f"Entitas '{entitas}' dengan ID '{id_entitas}' tidak ditemukan!", 404)

class SaldoTidakCukupError(AplikasiError):
    """Dilempar saat saldo pengguna kurang."""
    def __init__(self, saldo_ada: float, saldo_kurang: float) -> None:
        super().__init__(f"Saldo ada Rp {saldo_ada:,.2f}, dibutuhkan Rp {saldo_kurang:,.2f}")
        self.saldo_ada = saldo_ada
        self.saldo_kurang = saldo_kurang

def cari_produk(produk_id: int):
    if produk_id != 99:
        raise RecordNotFoundError("Produk", produk_id)
    return {"id": 99, "nama": "Kamera DSLR"}

try:
    cari_produk(42)
except RecordNotFoundError as e:
    print(f"Terjadi error spesifik: {e} (Status HTTP: {e.kode_status})")
except DatabaseError as e:
    print(f"Terjadi general db error: {e}")


# ------------------------------------------------------------------------------
# 3. Exception Chaining: 'raise ... from original_err' (PEP 3134)
# ------------------------------------------------------------------------------
print("\n--- [3] Exception Chaining (Pelestarian Traceback Asli) ---")

def hubungi_layanan_eksternal():
    try:
        # Simulasi kegagalan koneksi jaringan tingkat rendah
        raise ConnectionResetError("Socket reset by peer pada port 443")
    except ConnectionResetError as err_asli:
        # Wrap error sistem ke error bisnis kita dengan melestarikan root cause:
        raise DatabaseError("Gagal menghubungi cluster DB Replika") from err_asli

try:
    hubungi_layanan_eksternal()
except DatabaseError as e:
    print(f"Error Tertangkap: {e}")
    print(f"Penyebab Akar (Root Cause / __cause__): {e.__cause__}")


# ------------------------------------------------------------------------------
# 4. Fitur Modern Python 3.11+: ExceptionGroup & except*
# ------------------------------------------------------------------------------
print("\n--- [4] ExceptionGroup (Handling Concurrent Multi-Errors) ---")

def simulasi_multi_task_concurrent():
    daftar_error = [
        ValueError("Format payload task 1 salah"),
        KeyError("Field 'token' task 2 hilang"),
        ValueError("Angka negatif pada task 3")
    ]
    # Membungkus beberapa exception sekaligus ke dalam satu grup
    raise ExceptionGroup("Beberapa error terjadi bersamaan dalam worker pool", daftar_error)

try:
    simulasi_multi_task_concurrent()
except* ValueError as eg:
    # except* menangani subset error bertipe ValueError dari grup
    print(f"👉 Menangani {len(eg.exceptions)} ValueError: {[str(e) for e in eg.exceptions]}")
except* KeyError as eg:
    print(f"👉 Menangani {len(eg.exceptions)} KeyError: {[str(e) for e in eg.exceptions]}")


# ------------------------------------------------------------------------------
# 5. contextlib.suppress: Mengabaikan Exception Tertentu secara Pythonic
# ------------------------------------------------------------------------------
print("\n--- [5] contextlib.suppress ---")
# Menghilangkan kode boilerplate: try: ... except FileNotFoundError: pass
data_dict = {"a": 1}

with suppress(KeyError):
    del data_dict["kunci_yang_tidak_ada"]
print("Eksekusi berlanjut aman tanpa crash menggunakan suppress(KeyError).")


print("\n" + "=" * 70)
print("✅ KESIMPULAN & BEST PRACTICE FILE 04:")
print("1. Jangan pernah menggunakan `except:` kosong tanpa menyebutkan tipe Exception.")
print("2. Gunakan `else` untuk logika yang seharusnya HANYA jalan jika blok `try` berhasil.")
print("3. Selalu wariskan Custom Exception dari `Exception` (bukan `BaseException`).")
print("4. Gunakan `raise CustomError(...) from error_awal` agar jejak root cause tetap terlacak.")
print("5. Gunakan `except*` untuk concurrency (asyncio TaskGroup) di Python 3.11+.")
print("=" * 70)
