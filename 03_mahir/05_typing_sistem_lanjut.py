"""
================================================================================
MODUL 03: TINGKAT MAHIR (ADVANCED PYTHON)
FILE 05: Modern Type System: Generics, Protocols, TypeGuard & ParamSpec
================================================================================
Tujuan Pembelajaran:
1. Memahami Generic Programming dengan TypeVar.
2. Structural Subtyping (Duck Typing) menggunakan typing.Protocol.
3. Menjamin struktur payload JSON dengan TypedDict.
4. Nilai pasti dengan Literal and Type Narrowing via TypeGuard.
5. Menjaga presisi signature decorator menggunakan ParamSpec.
================================================================================
"""

from typing import (
    TypeVar,
    Generic,
    Protocol,
    TypedDict,
    Literal,
    TypeGuard,
    Callable,
    ParamSpec,
    runtime_checkable,
)

print("=" * 70)
print("--- [1] Generic Classes & Functions (TypeVar) ---")

T = TypeVar("T")  # Representasi tipe generik apa saja

class WadahPenyimpanan(Generic[T]):
    """Class generik yang dapat menampung elemen dengan tipe apa pun secara konsisten."""
    def __init__(self, item_awal: T) -> None:
        self._item: T = item_awal

    def get_item(self) -> T:
        return self._item

    def set_item(self, item_baru: T) -> None:
        self._item = item_baru

wadah_int = WadahPenyimpanan[int](100)
wadah_str = WadahPenyimpanan[str]("Token-XYZ")

print(f"Wadah Int: {wadah_int.get_item()} ({type(wadah_int.get_item()).__name__})")
print(f"Wadah Str: {wadah_str.get_item()} ({type(wadah_str.get_item()).__name__})")


# ------------------------------------------------------------------------------
# 2. Structural Subtyping dengan Protocol (Duck Typing Formal)
# ------------------------------------------------------------------------------
print("\n--- [2] typing.Protocol: Kontrak Berbasis Struktur Tanpa Inheritance ---")

@runtime_checkable
class DapatDirencanakan(Protocol):
    """Benda apa pun yang memiliki method .eksekusi() dianggap memenuhi protokol ini."""
    def eksekusi(self) -> str:
        ...

class TaskSistem:
    def eksekusi(self) -> str:
        return "TaskSistem berjalan normal."

class RobotPembersih:
    # Perhatikan: Class ini TIDAK mewarisi DapatDirencanakan secara eksplisit!
    def eksekusi(self) -> str:
        return "Robot membersihkan ruangan."

def jalankan_jadwal(pekerjaan: DapatDirencanakan) -> None:
    print(f"Hasil: {pekerjaan.eksekusi()}")

# Keduanya valid karena memenuhi struktur protokol (Structural Typing):
jalankan_jadwal(TaskSistem())
jalankan_jadwal(RobotPembersih())
print(f"Robot instanceof DapatDirencanakan? {isinstance(RobotPembersih(), DapatDirencanakan)}")


# ------------------------------------------------------------------------------
# 3. TypedDict, Literal & TypeGuard
# ------------------------------------------------------------------------------
print("\n--- [3] TypedDict, Literal & TypeGuard ---")

# Menentukan bentuk persis dari sebuah dictionary
class ResponAPI(TypedDict):
    status: Literal["SUCCESS", "FAILED", "PENDING"]
    kode: int
    pesan: str

# TypeGuard mempersempit (narrowing) tipe data saat analisis statis
def is_respon_sukses(resp: ResponAPI) -> TypeGuard[ResponAPI]:
    return resp["status"] == "SUCCESS"

respon_data: ResponAPI = {
    "status": "SUCCESS",
    "kode": 200,
    "pesan": "Operasi penarikan dana berhasil disetujui."
}

if is_respon_sukses(respon_data):
    print(f"✅ Transaksi Berhasil: {respon_data['pesan']}")


# ------------------------------------------------------------------------------
# 4. ParamSpec: Preservasi Tipe Parameter Decorator
# ------------------------------------------------------------------------------
print("\n--- [4] ParamSpec untuk Signature Decorator yang Akurat ---")

P = ParamSpec("P")
R = TypeVar("R")

def decorator_audit(func: Callable[P, R]) -> Callable[P, R]:
    """Decorator ini menjamin input params (P) dan return type (R) fungsi asli tidak hilang."""
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"🛡️  [AUDIT] Memanggil: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@decorator_audit
def transfer_dana(pengirim: str, penerima: str, jumlah: float) -> bool:
    print(f"Transfer Rp {jumlah:,.2f} dari {pengirim} ke {penerima}")
    return True

transfer_dana("Alice", "Bob", 500_000.0)


print("\n" + "=" * 70)
print("✅ KESIMPULAN & BEST PRACTICE FILE 05 (MAHIR):")
print("1. Gunakan `Protocol` untuk decoupled interfaces tanpa hierarki inheritance yang kaku.")
print("2. Gunakan `TypedDict` untuk representasi data dictionary bawaan JSON yang memiliki struktur pasti.")
print("3. Gunakan `Literal` untuk membatasi opsi string menjadi enum-like values.")
print("4. Gunakan `ParamSpec` pada setiap custom decorator ber-type hint agar IDE IntelliSense tetap berfungsi.")
print("=" * 70)
