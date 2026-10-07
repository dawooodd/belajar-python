"""
================================================================================
MODUL 03: TINGKAT MAHIR (ADVANCED PYTHON)
FILE 01: Metaprogramming, Descriptors Protocol, Metaclasses & __init_subclass__
================================================================================
Tujuan Pembelajaran:
1. Menguasai The Descriptor Protocol: __get__, __set__, __set_name__.
2. Memahami cara kerja internal @property dan implementasi ORM Field Validator.
3. Memahami konsep Metaclass: type sebagai instantiator dari class itu sendiri.
4. Membuat Metaclass untuk Singleton Pattern dan Registry Otomatis.
5. Modern alternative: __init_subclass__ (PEP 487) untuk arsitektur plugin.
================================================================================
"""

from typing import Any, Type

print("=" * 70)
print("--- [1] Descriptor Protocol: Membangun ORM Field Validator ---")

# Descriptor memungkinkan kita mencegat akses atribut pada level kelas
class ValidasiIntegerPositif:
    """Descriptor untuk memastikan atribut selalu bertipe integer dan bernilai positif."""
    
    def __set_name__(self, owner: Type[Any], name: str) -> None:
        # Dipanggil otomatis saat class dibuat (Python 3.6+)
        self.nama_privat = f"_{name}"
        self.nama_publik = name

    def __get__(self, instance: Any, owner: Type[Any]) -> Any:
        if instance is None:
            return self  # Dipanggil dari level Class (contoh: Model.umur)
        return getattr(instance, self.nama_privat, 0)

    def __set__(self, instance: Any, value: Any) -> None:
        if not isinstance(value, int):
            raise TypeError(f"Atribut '{self.nama_publik}' harus berupa integer! Mendapat: {type(value).__name__}")
        if value <= 0:
            raise ValueError(f"Atribut '{self.nama_publik}' harus bernilai positif (> 0)!")
        setattr(instance, self.nama_privat, value)


class ProdukModel:
    # Menggunakan descriptor seperti field pada Django ORM / SQLAlchemy
    harga = ValidasiIntegerPositif()
    stok = ValidasiIntegerPositif()

    def __init__(self, nama: str, harga: int, stok: int) -> None:
        self.nama = nama
        self.harga = harga  # Memicu descriptor __set__
        self.stok = stok

p = ProdukModel("Monitor Ultrawide", 4_500_000, 15)
print(f"Produk: {p.nama}, Harga: Rp {p.harga:,}, Stok: {p.stok}")

# Menguji validasi descriptor
try:
    p.harga = -500  # ❌ ValueError
except ValueError as e:
    print(f"Descriptor menolak nilai tidak valid: {e}")


# ------------------------------------------------------------------------------
# 2. Metaclass: Class yang Membuat Class
# ------------------------------------------------------------------------------
print("\n--- [2] Metaclass: Singleton Pattern pada Level Arsitektur ---")
# Di Python, sebuah class adalah instance dari metaclass 'type'.

class SingletonMeta(type):
    """Metaclass yang menjamin sebuah Class hanya memiliki 1 instance di seluruh memori."""
    _instances: dict[type, Any] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            # Memanggil implementasi __new__ & __init__ instance pertama kali
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class DatabasePool(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.koneksi_id = id(self)
        print(f"🔌 Inisialisasi DatabasePool baru dibuat (ID: {self.koneksi_id})")

pool1 = DatabasePool()
pool2 = DatabasePool()

print(f"Apakah pool1 is pool2? {pool1 is pool2} (Objek singleton identik di memori)")


# ------------------------------------------------------------------------------
# 3. Modern Pattern: __init_subclass__ (PEP 487)
# ------------------------------------------------------------------------------
print("\n--- [3] Plugin Registry dengan __init_subclass__ ---")
# __init_subclass__ adalah alternatif modern yang jauh lebih bersih daripada metaclass
# untuk mendaftarkan subclass secara otomatis.

class PluginBase:
    registry: dict[str, Type["PluginBase"]] = {}

    def __init_subclass__(cls, kode_plugin: str, **kwargs):
        super().__init_subclass__(**kwargs)
        # Otomatis mendaftarkan setiap class anak yang mewarisi PluginBase
        cls.registry[kode_plugin] = cls
        print(f"🔌 Plugin baru terdaftar otomatis: '{kode_plugin}' -> {cls.__name__}")


class PluginPembayaranOVO(PluginBase, kode_plugin="ovo"):
    def proses(self):
        return "Memproses via OVO"

class PluginPembayaranGoPay(PluginBase, kode_plugin="gopay"):
    def proses(self):
        return "Memproses via GoPay"

print(f"\nDaftar Registry Plugin Terkumpul: {PluginBase.registry}")


print("\n" + "=" * 70)
print("✅ KESIMPULAN & BEST PRACTICE FILE 01 (MAHIR):")
print("1. Gunakan Descriptors saat Anda membuat library, ORM, atau validasi field deklaratif.")
print("2. `__set_name__` mengeliminasi kebutuhan boilerplate penamaan variabel privat.")
print("3. Hindari Metaclass kecuali benar-benar diperlukan; 95% kasus dapat diselesaikan dengan `__init_subclass__`.")
print("=" * 70)
