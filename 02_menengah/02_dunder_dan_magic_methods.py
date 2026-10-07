"""
================================================================================
MODUL 02: TINGKAT MENENGAH (INTERMEDIATE PYTHON)
FILE 02: Dunder Methods (Magic Methods) & Python Data Model
================================================================================
Tujuan Pembelajaran:
1. Memahami peran Dunder Methods dalam mewujudkan filosofi "Python Data Model".
2. Menguasai representasi objek: __str__ vs __repr__.
3. Equality dan Hashability: __eq__ dan __hash__ (Objek kustom dalam Set/Dict).
4. Operator Overloading: __add__, __sub__, __mul__.
5. Emulasi Container: __len__, __getitem__, __contains__.
6. Callable Objects (__call__) dan Context Managers (__enter__, __exit__).
================================================================================
"""

import math
import time
from typing import Iterator

print("=" * 70)
print("--- [1] Operator Overloading & Representasi: Vektor 2D ---")

class Vektor2D:
    """Implementasi vektor matematika 2 dimensi dengan Dunder methods."""

    def __init__(self, x: float, y: float) -> None:
        self.x = float(x)
        self.y = float(y)

    # __repr__: Representasi resmi kode (bisa di-eval balik menjadi objek)
    def __repr__(self) -> str:
        return f"Vektor2D({self.x}, {self.y})"

    # __str__: Representasi ramah pengguna untuk print()
    def __str__(self) -> str:
        return f"({self.x}i + {self.y}j)"

    # Overload operator tambah (+)
    def __add__(self, other: "Vektor2D") -> "Vektor2D":
        if not isinstance(other, Vektor2D):
            return NotImplemented
        return Vektor2D(self.x + other.x, self.y + other.y)

    # Overload operator kurang (-)
    def __sub__(self, other: "Vektor2D") -> "Vektor2D":
        if not isinstance(other, Vektor2D):
            return NotImplemented
        return Vektor2D(self.x - other.x, self.y - other.y)

    # Overload operator perkalian skalar (*)
    def __mul__(self, skalar: float | int) -> "Vektor2D":
        if isinstance(skalar, (int, float)):
            return Vektor2D(self.x * skalar, self.y * skalar)
        return NotImplemented

    # Overload operator perbandingan kesetaraan (==)
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vektor2D):
            return False
        return math.isclose(self.x, other.x) and math.isclose(self.y, other.y)

    # Overload abs() untuk menghitung magnitudo / panjang vektor
    def __abs__(self) -> float:
        return math.hypot(self.x, self.y)

    # __hash__: Memungkinkan objek disimpan di set atau sebagai key dictionary
    def __hash__(self) -> int:
        return hash((self.x, self.y))

v1 = Vektor2D(3, 4)
v2 = Vektor2D(1, 2)

print(f"Representasi str  : {str(v1)}")
print(f"Representasi repr : {repr(v1)}")
print(f"Penjumlahan (v1+v2): {v1 + v2}")
print(f"Pengurangan (v1-v2): {v1 - v2}")
print(f"Skalar (v1 * 3)   : {v1 * 3}")
print(f"Panjang abs(v1)   : {abs(v1)} (3, 4 -> 5.0)")

# Menggunakan objek dalam Set karena memiliki __eq__ dan __hash__
koleksi_vektor = {v1, v2, Vektor2D(3, 4)}
print(f"Jumlah elemen unik dalam Set: {len(koleksi_vektor)} (Duplikat (3,4) berhasil difilter)")


# ------------------------------------------------------------------------------
# 2. Emulasi Container: Custom Smart Dataset
# ------------------------------------------------------------------------------
print("\n--- [2] Emulasi Container (__len__, __getitem__, __contains__) ---")

class DatasetKatalog:
    def __init__(self, data: list[dict]) -> None:
        self._data = list(data)

    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self, index: int | slice):
        # Mendukung indexing biasa dan slicing [1:3]
        return self._data[index]

    def __contains__(self, item_nama: str) -> bool:
        # Mendukung sintaks: if "Laptop" in katalog:
        return any(d.get("nama") == item_nama for d in self._data)

    def __iter__(self) -> Iterator[dict]:
        # Mendukung perulangan: for item in katalog:
        return iter(self._data)

katalog = DatasetKatalog([
    {"id": 1, "nama": "Laptop", "harga": 15000000},
    {"id": 2, "nama": "Mouse", "harga": 300000},
    {"id": 3, "nama": "Keyboard", "harga": 750000},
])

print(f"Panjang Katalog (len): {len(katalog)}")
print(f"Index ke-0: {katalog[0]}")
print(f"Apakah 'Mouse' ada di katalog? {'Mouse' in katalog}")
print(f"Apakah 'Monitor' ada di katalog? {'Monitor' in katalog}")


# ------------------------------------------------------------------------------
# 3. Callable Objects (__call__)
# ------------------------------------------------------------------------------
print("\n--- [3] Callable Objects (__call__) ---")
# Menjadikan instance class dapat dieksekusi seperti fungsi biasa

class PengaliFaktor:
    def __init__(self, faktor: float) -> None:
        self.faktor = faktor

    def __call__(self, nilai: float) -> float:
        return nilai * self.faktor

kali_sepuluh = PengaliFaktor(10)
print(f"Pemanggilan instance sebagai fungsi: {kali_sepuluh(5)} (5 * 10)")


# ------------------------------------------------------------------------------
# 4. Context Manager Protocol (__enter__ & __exit__)
# ------------------------------------------------------------------------------
print("\n--- [4] Context Manager Kustom (with statement) ---")

class PengukurWaktu:
    """Mengukur durasi eksekusi kode dengan blok 'with'."""

    def __enter__(self):
        self.mulai = time.perf_counter()
        print("⏱️  [Mulai mengukur waktu...]")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.selesai = time.perf_counter()
        durasi = self.selesai - self.mulai
        print(f"⏱️  [Selesai!] Waktu eksekusi: {durasi * 1000:.3f} ms")
        # Return True jika ingin menekan (suppress) exception yang terjadi
        return False

with PengukurWaktu():
    # Simulasi komputasi
    total = sum(i ** 2 for i in range(100_000))
    print(f"Hasil kalkulasi sampel: {total}")


print("\n" + "=" * 70)
print("✅ KESIMPULAN & BEST PRACTICE FILE 02:")
print("1. Selalu implementasikan `__repr__` untuk mempermudah debugging dan logging.")
print("2. Jika Anda membuat `__eq__`, buat juga `__hash__` jika objek bersifat immutable.")
print("3. Gunakan `__getitem__` dan `__len__` untuk membuat objek kustom yang bertingkah seperti list/dict.")
print("4. Manfaatkan `__call__` untuk membuat objek yang menyimpan state sekaligus bertindak sebagai callable.")
print("5. Terapkan `__enter__` dan `__exit__` untuk pengelolaan resource (koneksi DB, file, locks).")
print("=" * 70)
