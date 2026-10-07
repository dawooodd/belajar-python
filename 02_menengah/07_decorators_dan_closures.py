"""
================================================================================
MODUL 02: TINGKAT MENENGAH (INTERMEDIATE PYTHON)
FILE 07: Closures, Decorators, Stacking & Produksi Decorator Patterns
================================================================================
Tujuan Pembelajaran:
1. Memahami Closures dan status memori first-class functions.
2. Mekanisme sintaks decorator (@) dan peran krusial @functools.wraps.
3. Membuat Decorator dengan parameter argumen (3-layer decorator).
4. Urutan eksekusi Decorator bertingkat (Stacking Decorators).
5. Implementasi real-world production decorators:
   - Pengukur Durasi Eksekusi (@catat_waktu)
   - Mekanisme Coba Ulang Otomatis (@retry)
   - Memoization / Caching Kustom
================================================================================
"""

import functools
import time
from typing import Callable, Any

print("=" * 70)
print("--- [1] Closures: Fungsi yang Mengingat Lingkungannya ---")

def buat_formatter(awalan: str) -> Callable[[str], str]:
    # Variabel 'awalan' terbungkus (closed over) di dalam fungsi internal
    def format_pesan(pesan: str) -> str:
        return f"[{awalan.upper()}] {pesan}"
    return format_pesan

log_info = buat_formatter("info")
log_error = buat_formatter("critical_error")

print(log_info("Server dimulai pada port 8000"))
print(log_error("Koneksi database terputus!"))


# ------------------------------------------------------------------------------
# 2. Anatomi Decorator & Peran Penting @functools.wraps
# ------------------------------------------------------------------------------
print("\n--- [2] Anatomi Decorator & functools.wraps ---")

def catat_eksekusi(func: Callable) -> Callable:
    # @functools.wraps menjaga __name__, __doc__, dan anotasi asli fungsi
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        print(f"👉 Menjalankan fungsi: '{func.__name__}' dengan args={args}, kwargs={kwargs}")
        hasil = func(*args, **kwargs)
        print(f"👈 Selesai '{func.__name__}', hasil: {hasil}")
        return hasil
    return wrapper

@catat_eksekusi
def tambah(a: int, b: int) -> int:
    """Menjumlahkan dua bilangan bulat."""
    return a + b

hasil_tambah = tambah(15, 35)
print(f"Hasil: {hasil_tambah}")
print(f"Nama Asli Fungsi: {tambah.__name__} (Tetap 'tambah', bukan 'wrapper')")
print(f"Docstring Asli  : {tambah.__doc__}")


# ------------------------------------------------------------------------------
# 3. Decorator dengan Parameter (Decorator Factory)
# ------------------------------------------------------------------------------
print("\n--- [3] Decorator dengan Parameter: Retry Pattern ---")

def ulangi(maksimal_coba: int = 3, jeda_detik: float = 0.5):
    """Decorator factory yang menerima argumen konfigurasi coba ulang."""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            percobaan = 0
            while percobaan < maksimal_coba:
                try:
                    percobaan += 1
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"⚠️  Percobaan #{percobaan} gagal ({e}). Menunggu {jeda_detik}s...")
                    time.sleep(jeda_detik)
                    if percobaan >= maksimal_coba:
                        print(f"❌ Gagal setelah {maksimal_coba} kali percobaan.")
                        raise
        return wrapper
    return decorator

percobaan_hitung = 0

@ulangi(maksimal_coba=3, jeda_detik=0.1)
def request_api_flaky() -> str:
    global percobaan_hitung
    percobaan_hitung += 1
    if percobaan_hitung < 3:
        raise ConnectionError("Server sibuk (503)")
    return "Data Payload Berhasil Diterima!"

hasil_api = request_api_flaky()
print(f"Hasil Akhir Retry: {hasil_api}")


# ------------------------------------------------------------------------------
# 4. Decorator Berbentuk Class (Class as Decorator)
# ------------------------------------------------------------------------------
print("\n--- [4] Class-Based Decorator untuk Memoization / Cache ---")

class CacheMemoize:
    """Menyimpan hasil fungsi murni di memori berdasarkan argumen."""
    def __init__(self, func: Callable) -> None:
        self.func = func
        self.cache: dict[tuple, Any] = {}
        functools.update_wrapper(self, func)

    def __call__(self, *args) -> Any:
        if args in self.cache:
            print(f"⚡ [CACHE HIT] Mengambil dari memori untuk argumen {args}")
            return self.cache[args]
        
        print(f"🔄 [CACHE MISS] Menghitung ulang untuk argumen {args}")
        hasil = self.func(*args)
        self.cache[args] = hasil
        return hasil

@CacheMemoize
def faktorial(n: int) -> int:
    return 1 if n <= 1 else n * faktorial(n - 1)

print("Hitung faktorial 4 pertama kali:")
print(f"Hasil: {faktorial(4)}")

print("\nHitung faktorial 4 kedua kali (seharusnya instan dari cache):")
print(f"Hasil: {faktorial(4)}")


print("\n" + "=" * 70)
print("✅ KESIMPULAN & BEST PRACTICE FILE 07:")
print("1. Selalu gunakan `@functools.wraps(func)` pada setiap decorator yang Anda ciptakan.")
print("2. Pahami 3 lapisan fungsi jika decorator Anda membutuhkan parameter input.")
print("3. Stacking decorator dieksekusi dari BAWAH ke ATAS saat inisialisasi.")
print("4. Gunakan class-based decorator jika Anda membutuhkan state yang kompleks dalam wrapper.")
print("=" * 70)
