"""
================================================================================
MODUL 03: TINGKAT MAHIR (ADVANCED PYTHON)
FILE 04: Manajemen Memori, Garbage Collection, Slots & Performance Profiling
================================================================================
Tujuan Pembelajaran:
1. Memahami mekanisme internal CPython: Reference Counting & Cyclic Garbage Collector.
2. Mendeteksi circular references menggunakan modul bawaan 'gc'.
3. Optimasi memori ekstrem dengan '__slots__' vs standard '__dict__'.
4. Tracing kebocoran memori (memory leak) dengan 'tracemalloc'.
5. Profiling kemacetan kode (CPU bottleneck) menggunakan 'cProfile' dan 'pstats'.
================================================================================
"""

import cProfile
import gc
import pstats
import sys
import tracemalloc
import timeit
from io import StringIO

print("=" * 70)
print("--- [1] Reference Counting & Cyclic Garbage Collection ---")

class NodeSiklik:
    def __init__(self, nama: str) -> None:
        self.nama = nama
        self.partner = None

    def __del__(self) -> None:
        pass  # Finalizer hook saat objek dihancurkan

# Membuat Circular Reference (A merujuk B, dan B merujuk A)
a = NodeSiklik("Node A")
b = NodeSiklik("Node B")
a.partner = b
b.partner = a

print(f"Ref count sebelum del: a={sys.getrefcount(a) - 1}, b={sys.getrefcount(b) - 1}")

# Hapus variabel lokal
del a
del b

# Objek masih ada di RAM karena saling merujuk (circular reference)!
# Garbage Collector siklis akan membersihkannya:
jumlah_sampah = gc.collect()
print(f"Garbage Collector menemukan & membersihkan {jumlah_sampah} objek siklis.")


# ------------------------------------------------------------------------------
# 2. Optimasi Memori: __slots__ vs Default __dict__
# ------------------------------------------------------------------------------
print("\n--- [2] Benchmark Memori: Standard Class vs __slots__ ---")

class KordinatBiasa:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z

class KordinatSlots:
    __slots__ = ("x", "y", "z")  # Menginstruksikan Python untuk tidak membuat __dict__
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z

# Mengukur alokasi memori untuk 100.000 objek
tracemalloc.start()
snap1 = tracemalloc.take_snapshot()
daftar_biasa = [KordinatBiasa(1.0, 2.0, 3.0) for _ in range(100_000)]
snap2 = tracemalloc.take_snapshot()
stat_biasa = snap2.compare_to(snap1, 'lineno')
alokasi_biasa = sum(stat.size_diff for stat in stat_biasa)

del daftar_biasa
gc.collect()

snap3 = tracemalloc.take_snapshot()
daftar_slots = [KordinatSlots(1.0, 2.0, 3.0) for _ in range(100_000)]
snap4 = tracemalloc.take_snapshot()
stat_slots = snap4.compare_to(snap3, 'lineno')
alokasi_slots = sum(stat.size_diff for stat in stat_slots)
tracemalloc.stop()

print(f"Alokasi Memori Class Biasa : {alokasi_biasa / (1024 * 1024):.2f} MB")
print(f"Alokasi Memori dengan Slots: {alokasi_slots / (1024 * 1024):.2f} MB")
print(f"Penghematan Memori         : {(1 - alokasi_slots / alokasi_biasa) * 100:.1f}%!")


# ------------------------------------------------------------------------------
# 3. CPU Profiling Menggunakan cProfile & pstats
# ------------------------------------------------------------------------------
print("\n--- [3] CPU Profiling dengan cProfile ---")

def kalkulasi_lambat():
    # Fungsi tiruan yang memakan waktu CPU
    total = 0
    for i in range(100_000):
        total += i ** 2
    return total

def alur_kerja_aplikasi():
    hasil1 = kalkulasi_lambat()
    hasil2 = [x for x in range(50_000) if x % 3 == 0]
    return hasil1, len(hasil2)

profiler = cProfile.Profile()
profiler.enable()

# Jalankan kode yang ingin dianalisis
alur_kerja_aplikasi()

profiler.disable()

# Format output statistik profiling
stream = StringIO()
stats = pstats.Stats(profiler, stream=stream).sort_stats(pstats.SortKey.CUMULATIVE)
stats.print_stats(5)  # Tampilkan 5 fungsi paling memakan waktu
print("Hasil Profiling (Top 5 Call Stacks):")
print(stream.getvalue().splitlines()[4:12])


print("\n" + "=" * 70)
print("✅ KESIMPULAN & BEST PRACTICE FILE 04 (MAHIR):")
print("1. Gunakan `__slots__` jika Anda membuat jutaan instance dari class kecil yang sama.")
print("2. Gunakan `tracemalloc` untuk melacak sumber kebocoran memori (memory leak).")
print("3. Selalu profil kode Anda dengan `cProfile` SEBELUM melakukan optimasi (hindari premature optimization).")
print("=" * 70)
