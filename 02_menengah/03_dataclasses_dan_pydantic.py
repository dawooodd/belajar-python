"""
================================================================================
MODUL 02: TINGKAT MENENGAH (INTERMEDIATE PYTHON)
FILE 03: Data Classes (@dataclass Modern) dan Validasi Skema Pydantic v2
================================================================================
Tujuan Pembelajaran:
1. Memahami efisiensi boilerplate dengan modul bawaan dataclasses.
2. Memanfaatkan fitur dataclass modern: slots=True, frozen=True, kw_only=True.
3. Kustomisasi field(default_factory=...) dan lifecycle hook __post_init__.
4. Menguasai Pydantic v2 untuk parsing data runtime, validasi, dan serialisasi JSON.
================================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
import sys
from pydantic import BaseModel, Field, field_validator, EmailStr

print("=" * 70)
print("--- [1] Modern @dataclass: slots=True & frozen=True ---")

# slots=True (Python 3.10+): Mengeliminasi __dict__ pada instance, menghemat
# memori hingga 40-50% dan mempercepat akses atribut secara drastis!
@dataclass(slots=True, frozen=True)
class TitikGeografis:
    latitude: float
    longitude: float
    nama_lokasi: str = "Tidak Diketahui"

lokasi_1 = TitikGeografis(-6.1754, 106.8272, "Monas Jakarta")
print(f"Data Geografis: {lokasi_1}")

# Karena frozen=True, objek bersifat immutable (tidak bisa diubah):
# lokasi_1.latitude = 0.0 # ❌ FrozenInstanceError!


# ------------------------------------------------------------------------------
# 2. Advanced Dataclass: default_factory, ordering & __post_init__
# ------------------------------------------------------------------------------
print("\n--- [2] Advanced Dataclass (__post_init__ & ordering) ---")

@dataclass(order=True)
class ItemPesanan:
    # Urutan sorting didasarkan pada total_harga (sort_index)
    sort_index: float = field(init=False, repr=False)
    nama_barang: str = field(compare=False)
    harga_satuan: float = field(compare=False)
    kuantitas: int = field(compare=False, default=1)
    tags: list[str] = field(default_factory=list, compare=False)

    def __post_init__(self) -> None:
        """Dijalankan otomatis setelah __init__ bawaan selesai."""
        if self.harga_satuan < 0 or self.kuantitas <= 0:
            raise ValueError("Harga satuan dan kuantitas harus valid!")
        # Mengisi sort_index untuk perbandingan otomatis
        self.sort_index = self.harga_satuan * self.kuantitas

    @property
    def total_harga(self) -> float:
        return self.harga_satuan * self.kuantitas

item_a = ItemPesanan("Mouse Wireless", 250_000, 2)
item_b = ItemPesanan("Mechanical Keyboard", 1_200_000, 1)
item_c = ItemPesanan("Mousepad Gaming", 150_000, 1)

daftar_belanja = [item_a, item_b, item_c]
daftar_belanja_urut = sorted(daftar_belanja)

print("Daftar pesanan diurutkan berdasarkan total harga:")
for item in daftar_belanja_urut:
    print(f"- {item.nama_barang:<22}: Rp {item.total_harga:>10,}")


# ------------------------------------------------------------------------------
# 3. Pydantic v2: Validasi Runtime & Parsing Data API
# ------------------------------------------------------------------------------
print("\n--- [3] Pydantic v2: Validasi Data Runtime Skala Produksi ---")

class PenggunaRegistrasiSchema(BaseModel):
    username: str = Field(min_length=3, max_length=20, description="Username unik")
    email: str = Field(description="Email pengguna")
    umur: int = Field(ge=17, le=100, description="Umur minimal 17 tahun")
    saldo_dompet: float = Field(default=0.0, ge=0.0)
    aktif: bool = True
    dibuat_pada: datetime = Field(default_factory=datetime.now)

    @field_validator("username")
    @classmethod
    def username_harus_alphanumeric(cls, value: str) -> str:
        if not value.isalnum():
            raise ValueError("Username hanya boleh terdiri dari huruf dan angka!")
        return value.lower()

    @field_validator("email")
    @classmethod
    def email_harus_valid(cls, value: str) -> str:
        if "@" not in value or "." not in value:
            raise ValueError("Format email tidak valid!")
        return value.lower()

# Simulasi Payload JSON mentah dari Frontend (string coercion otomatis)
payload_mentah = {
    "username": "SuperUser99",
    "email": "SUPERUSER@Example.COM",
    "umur": "24",            # String '24' akan di-cast otomatis menjadi int 24
    "saldo_dompet": "150000.50"
}

try:
    user_tervalidasi = PenggunaRegistrasiSchema(**payload_mentah)
    print("✅ Validasi Pydantic Berhasil!")
    print(f"Hasil Model: {user_tervalidasi}")
    print(f"Tipe Umur setelah parsing: {type(user_tervalidasi.umur).__name__}")
    
    # Export ke JSON murni
    print(f"\nJSON Output: {user_tervalidasi.model_dump_json(indent=2)}")
except Exception as e:
    print(f"❌ Validasi Gagal: {e}")

# Simulasi Payload yang Tidak Valid (Menangkap Error Detail)
print("\nMenguji Input yang Melanggar Aturan Bisnis:")
try:
    PenggunaRegistrasiSchema(username="ab", email="bukan_email", umur=15)
except Exception as e:
    print(f"Validasi berhasil menolak input buruk:\n{e}")


print("\n" + "=" * 70)
print("✅ KESIMPULAN & BEST PRACTICE FILE 03:")
print("1. Gunakan `@dataclass(slots=True)` untuk struktur data internal berkecepatan tinggi.")
print("2. Gunakan `field(default_factory=list)` untuk mencegah bug mutable default argument.")
print("3. Gunakan Pydantic untuk data eksternal yang tidak terpercaya (API request, env var, config file).")
print("4. Manfaatkan `@field_validator` untuk penegakan aturan bisnis secara deklaratif.")
print("=" * 70)
