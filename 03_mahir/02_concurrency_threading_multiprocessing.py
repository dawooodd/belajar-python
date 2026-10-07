"""
================================================================================
MODUL 03: TINGKAT MAHIR (ADVANCED PYTHON)
FILE 02: Concurrency, GIL, Threading, Multiprocessing & Concurrent Futures
================================================================================
Tujuan Pembelajaran:
1. Memahami Global Interpreter Lock (GIL) di CPython dan evolusinya (PEP 703).
2. Membedakan tugas I/O-Bound (jaringan/disk) vs CPU-Bound (kalkulasi murni).
3. Menggunakan ThreadPoolExecutor untuk I/O-Bound concurrency.
4. Menghindari Race Condition menggunakan threading.Lock.
5. Menggunakan ProcessPoolExecutor untuk memanfaatkan Multi-Core CPU penuh.
================================================================================
"""

import concurrent.futures
import threading
import time
import math
from typing import List

print("=" * 70)
print("--- [1] GIL & Analisis Karakteristik Tugas ---")
print("Teori Penting:")
print("- I/O-Bound : Waktu dihabiskan menunggu network/file/DB. Solusi: THREADING / ASYNCIO.")
print("- CPU-Bound : Waktu dihabiskan menghitung di prosesor. Solusi: MULTIPROCESSING.")
print("=" * 70)


# ------------------------------------------------------------------------------
# 2. ThreadPoolExecutor untuk Tugas I/O Bound
# ------------------------------------------------------------------------------
print("\n--- [2] Simulasi I/O-Bound: Multi-Threaded Web Scraper / Downloader ---")

def unduh_data_simulasi(url: str) -> dict:
    waktu_mulai = time.perf_counter()
    # Simulasi latensi jaringan (I/O wait)
    time.sleep(0.3)
    durasi = time.perf_counter() - waktu_mulai
    return {"url": url, "status": 200, "durasi_detik": round(durasi, 3)}

daftar_url = [f"https://api.example.com/data/{i}" for i in range(1, 6)]

# Menjalankan secara paralel dengan ThreadPoolExecutor
mulai_io = time.perf_counter()
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    hasil_io = list(executor.map(unduh_data_simulasi, daftar_url))

total_waktu_io = time.perf_counter() - mulai_io
print(f"5 Request selesai dalam {total_waktu_io:.3f} detik (Secara sekuensial akan butuh 1.5 detik!)")
for res in hasil_io:
    print(f"  -> {res['url']}: Status {res['status']} ({res['durasi_detik']}s)")


# ------------------------------------------------------------------------------
# 3. Race Condition & Solusi dengan threading.Lock
# ------------------------------------------------------------------------------
print("\n--- [3] Sinkronisasi Shared State dengan threading.Lock ---")

class SaldoBankAman:
    def __init__(self) -> None:
        self.saldo = 0
        self.lock = threading.Lock()

    def tambah_saldo(self, nominal: int) -> None:
        with self.lock:  # Memastikan hanya 1 thread yang memutasi saldo dalam satu waktu
            saldo_sementara = self.saldo
            time.sleep(0.0001)  # Sengaja memicu context switch
            self.saldo = saldo_sementara + nominal

bank = SaldoBankAman()
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    # 50 thread menambahkan Rp 10.000 secara serentak
    futures = [executor.submit(bank.tambah_saldo, 10_000) for _ in range(50)]
    concurrent.futures.wait(futures)

print(f"Saldo Akhir (dengan Mutex Lock): Rp {bank.saldo:,} (Sempurna: 50 * 10,000 = 500,000)")


# ------------------------------------------------------------------------------
# 4. ProcessPoolExecutor untuk Tugas Berat CPU-Bound
# ------------------------------------------------------------------------------
def faktorisasi_prima_berat(n: int) -> int:
    """Komputasi matematika intensif murni membebani prosesor."""
    hitung = 0
    for i in range(2, 500_000):
        if i % 2 == 0:
            hitung += 1
    return hitung

def demo_multiprocessing():
    print("\n--- [4] CPU-Bound Paralel: ProcessPoolExecutor ---")
    data_input = [1, 2, 3, 4]
    
    mulai_cpu = time.perf_counter()
    # Menggunakan multi-process yang melewati batasan GIL CPython
    with concurrent.futures.ProcessPoolExecutor() as executor:
        hasil_cpu = list(executor.map(faktorisasi_prima_berat, data_input))
    durasi_cpu = time.perf_counter() - mulai_cpu
    print(f"Kalkulasi berat pada 4 core selesai dalam: {durasi_cpu:.3f} detik")


if __name__ == "__main__":
    demo_multiprocessing()
    print("\n" + "=" * 70)
    print("✅ KESIMPULAN & BEST PRACTICE FILE 02 (MAHIR):")
    print("1. Gunakan ThreadPoolExecutor untuk memanggil HTTP API eksternal atau membaca banyak file.")
    print("2. Selalu gunakan `threading.Lock` saat memodifikasi shared variable antar thread.")
    print("3. Gunakan ProcessPoolExecutor untuk komputasi matematika, pemrosesan citra, atau data sains.")
    print("4. Selalu tempatkan kode multiprocessing di bawah blok `if __name__ == '__main__':` di Windows.")
    print("=" * 70)
