"""
================================================================================
MODUL 02: TINGKAT MENENGAH (INTERMEDIATE PYTHON)
FILE 06: Iterators, Generators, Yield From & Pemrosesan Streaming Data
================================================================================
Tujuan Pembelajaran:
1. Memahami protokol Iterator: __iter__(), __next__(), dan StopIteration.
2. Membedakan Iterable vs Iterator.
3. Generator Functions (yield) dan Generator Expressions.
4. Tolok ukur hemat memori: List vs Generator (juta data).
5. Generator Delegation dengan 'yield from'.
6. Membangun Data Pipeline gaya Unix Pipe secara efisien.
================================================================================
"""

import sys
import time
from typing import Iterator

print("=" * 70)
print("--- [1] Protokol Iterator Manual ---")

class DeretHitungMundur:
    """Implementasi protokol iterator secara manual dari nol."""
    def __init__(self, mulai: int) -> None:
        self.sekarang = mulai

    def __iter__(self) -> "DeretHitungMundur":
        return self

    def __next__(self) -> int:
        if self.sekarang <= 0:
            raise StopIteration
        nilai = self.sekarang
        self.sekarang -= 1
        return nilai

deret = DeretHitungMundur(3)
print(f"Manual next 1: {next(deret)}")
print(f"Manual next 2: {next(deret)}")
print(f"Manual next 3: {next(deret)}")
# Pemanggilan berikutnya akan raise StopIteration


# ------------------------------------------------------------------------------
# 2. Generator Function (yield) & Generator Expressions
# ------------------------------------------------------------------------------
print("\n--- [2] Generator Function (yield) ---")

def generator_fibonacci(batas_n: int) -> Iterator[int]:
    """Menghasilkan bilangan Fibonacci secara on-demand (lazy evaluation)."""
    a, b = 0, 1
    for _ in range(batas_n):
        yield a
        a, b = b, a + b

print("10 Bilangan Fibonacci Pertama:")
for angka in generator_fibonacci(10):
    print(angka, end=" ")
print()


# ------------------------------------------------------------------------------
# 3. Benchmark Memori: List Comprehension vs Generator Expression
# ------------------------------------------------------------------------------
print("\n--- [3] Perbandingan Memori: List vs Generator (10 Juta Elemen) ---")

N = 10_000_000

# Generator Expression: TIDAK menyimpan data ke RAM secara sekaligus
gen_expr = (x * 2 for x in range(N))
ukuran_gen = sys.getsizeof(gen_expr)

print(f"Ukuran Memori Generator Expression : {ukuran_gen} bytes (~{ukuran_gen / 1024:.2f} KB)")
print("Koleksi list 10 juta elemen akan menghabiskan >80 MB RAM!")
print(f"Mengambil 3 elemen pertama dari generator: {[next(gen_expr) for _ in range(3)]}")


# ------------------------------------------------------------------------------
# 4. yield from (Sub-generator Delegation)
# ------------------------------------------------------------------------------
print("\n--- [4] Generator Delegation dengan 'yield from' ---")

def pecahan_a():
    yield "A1"
    yield "A2"

def pecahan_b():
    yield "B1"
    yield "B2"

def gabungan_generator():
    yield "START"
    yield from pecahan_a() # Mendelegasikan iterasi ke pecahan_a
    yield from pecahan_b() # Mendelegasikan iterasi ke pecahan_b
    yield "FINISH"

print("Hasil gabungan generator:")
for item in gabungan_generator():
    print(f"- {item}")


# ------------------------------------------------------------------------------
# 5. Arsitektur Data Processing Pipeline (Gaya Unix Pipe)
# ------------------------------------------------------------------------------
print("\n--- [5] Data Streaming Pipeline Tanpa Membebani RAM ---")
# Kasus: Membaca log server jutaan baris, memfilter error, mengekstrak IP

baris_log_dummy = [
    '2026-10-07 10:00:01 INFO [192.168.1.10] User login',
    '2026-10-07 10:00:05 ERROR [10.0.0.5] Database connection timeout',
    '2026-10-07 10:00:10 WARN [192.168.1.15] Memory usage 85%',
    '2026-10-07 10:00:15 ERROR [172.16.0.4] Authentication failed',
    '2026-10-07 10:00:20 INFO [192.168.1.10] User logout',
]

# Tahap 1: Generator pembaca baris
def baca_baris(logs: list[str]) -> Iterator[str]:
    for baris in logs:
        yield baris

# Tahap 2: Filter baris hanya tipe ERROR
def filter_error(stream: Iterator[str]) -> Iterator[str]:
    for baris in stream:
        if "ERROR" in baris:
            yield baris

# Tahap 3: Ekstraksi IP
def ekstrak_ip(stream: Iterator[str]) -> Iterator[str]:
    for baris in stream:
        bagian_ip = baris.split("[")[1].split("]")[0]
        yield bagian_ip

# Menyambungkan pipa (pipeline):
aliran_log = baca_baris(baris_log_dummy)
aliran_error = filter_error(aliran_log)
aliran_ip_error = ekstrak_ip(aliran_error)

print("IP yang memicu status ERROR:")
for ip in aliran_ip_error:
    print(f"🚨 Terdeteksi IP Error: {ip}")


print("\n" + "=" * 70)
print("✅ KESIMPULAN & BEST PRACTICE FILE 06:")
print("1. Gunakan generator untuk dataset berukuran besar atau stream kontinu (mencegah Out of Memory).")
print("2. Gunakan tanda kurung `(x for x in ...)` alih-alih `[x for x in ...]` jika hanya ingin diiterasi sekali.")
print("3. Manfaatkan `yield from` saat mendistribusikan iterasi pohon (tree) atau nested iterable.")
print("4. Buat generator modular untuk memproses pipeline data bertingkat (extract -> filter -> transform).")
print("=" * 70)
