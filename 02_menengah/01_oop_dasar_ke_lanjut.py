"""
================================================================================
MODUL 02: TINGKAT MENENGAH (INTERMEDIATE PYTHON)
FILE 01: Pemrograman Berorientasi Objek (OOP) dari Dasar ke Tingkat Lanjut
================================================================================
Tujuan Pembelajaran:
1. Memahami 4 Pilar OOP: Enkapsulasi, Abstraksi, Pewarisan, dan Polimorfisme.
2. Property Decorators (@property, @setter) untuk enkapsulasi yang elegan.
3. Perbedaan Instance Method, @classmethod, dan @staticmethod.
4. Multiple Inheritance dan Method Resolution Order (MRO) dengan C3 Linearization.
5. Abstract Base Classes (ABC) dan penegakan antarmuka (interface contract).
================================================================================
"""

from abc import ABC, abstractmethod
from typing import ClassVar

print("=" * 70)
print("--- [1] Enkapsulasi, Name Mangling & Property Decorator ---")

class RekeningBank:
    """Contoh implementasi enkapsulasi ketat pada rekening perbankan."""
    
    # Class Variable (dishare oleh seluruh instance)
    total_akun_terdaftar: ClassVar[int] = 0
    SUKU_BUNGA_TAHUNAN: ClassVar[float] = 0.05

    def __init__(self, pemilik: str, saldo_awal: float = 0.0) -> None:
        self.pemilik: str = pemilik              # Atribut Publik
        self._nomor_rekening: str = "ACC-" + str(RekeningBank.total_akun_terdaftar + 1001) # Protected (Konvensi)
        self.__saldo: float = max(0.0, saldo_awal) # Private (Memicu Name Mangling: _RekeningBank__saldo)
        
        RekeningBank.total_akun_terdaftar += 1

    # Getter menggunakan @property
    @property
    def saldo(self) -> float:
        """Mengambil saldo secara aman."""
        return self.__saldo

    # Setter menggunakan @saldo.setter dengan validasi bisnis
    @saldo.setter
    def saldo(self, nilai_baru: float) -> None:
        if nilai_baru < 0:
            raise ValueError("Saldo tidak boleh negatif!")
        self.__saldo = nilai_baru

    def setor(self, jumlah: float) -> None:
        if jumlah <= 0:
            raise ValueError("Jumlah setoran harus positif!")
        self.__saldo += jumlah

    def tarik(self, jumlah: float) -> bool:
        if 0 < jumlah <= self.__saldo:
            self.__saldo -= jumlah
            return True
        return False

    # Class Method: Factory method atau memanipulasi Class Variable
    @classmethod
    def buat_akun_promo(cls, pemilik: str) -> "RekeningBank":
        """Factory method yang memberikan bonus saldo awal Rp 50.000."""
        return cls(pemilik, saldo_awal=50_000.0)

    # Static Method: Fungsi utilitas murni yang tidak menyentuh self maupun cls
    @staticmethod
    def validasi_format_ktp(nomor_ktp: str) -> bool:
        return len(nomor_ktp) == 16 and nomor_ktp.isdigit()

rek1 = RekeningBank("Budi Santoso", 250_000.0)
rek_promo = RekeningBank.buat_akun_promo("Siti Rahma")

print(f"Pemilik Rek 1: {rek1.pemilik}, Saldo: Rp {rek1.saldo:,.2f}")
rek1.setor(150_000)
print(f"Saldo setelah setor: Rp {rek1.saldo:,.2f}")

# Demonstrasi name mangling
print(f"Akses private via mangling: {rek1._RekeningBank__saldo:,.2f}")
print(f"Validasi KTP Static: {RekeningBank.validasi_format_ktp('3201123456789012')}")
print(f"Total akun dibuat: {RekeningBank.total_akun_terdaftar}")


# ------------------------------------------------------------------------------
# 2. Abstraksi: Abstract Base Class (ABC)
# ------------------------------------------------------------------------------
print("\n--- [2] Abstract Base Class (ABC) & Polimorfisme Kontrak ---")

class GatewayPembayaran(ABC):
    """Interface abstrak yang mewajibkan semua gateway turunan mengimplementasikannya."""
    
    @abstractmethod
    def proses_bayar(self, nominal: float) -> dict[str, str | float]:
        """Setiap payment provider harus mengimplementasikan fungsi ini."""
        pass

    @abstractmethod
    def refund(self, transaksi_id: str) -> bool:
        pass


class MidtransGateway(GatewayPembayaran):
    def proses_bayar(self, nominal: float) -> dict[str, str | float]:
        return {"status": "SUCCESS", "gateway": "Midtrans", "gross_amount": nominal}

    def refund(self, transaksi_id: str) -> bool:
        print(f"[Midtrans] Melakukan refund ID: {transaksi_id}")
        return True


class XenditGateway(GatewayPembayaran):
    def proses_bayar(self, nominal: float) -> dict[str, str | float]:
        return {"status": "PAID", "gateway": "Xendit", "charge": nominal}

    def refund(self, transaksi_id: str) -> bool:
        print(f"[Xendit] Melakukan refund ID: {transaksi_id}")
        return True


def checkout_pesanan(gateway: GatewayPembayaran, total: float):
    # Polimorfisme: checkout_pesanan tidak peduli vendor apa, asalkan mematuhi kontrak
    hasil = gateway.proses_bayar(total)
    print(f"Hasil Checkout: {hasil}")

checkout_pesanan(MidtransGateway(), 750_000)
checkout_pesanan(XenditGateway(), 1_250_000)


# ------------------------------------------------------------------------------
# 3. Pewarisan Berganda & Method Resolution Order (MRO)
# ------------------------------------------------------------------------------
print("\n--- [3] Multiple Inheritance & C3 Linearization (MRO) ---")
# Masalah Diamond Problem diatasi Python dengan algoritma C3 linearization

class LoggerMixin:
    def log(self, pesan: str) -> None:
        print(f"[LOG: {self.__class__.__name__}]: {pesan}")


class SerializerMixin:
    def to_dict(self) -> dict:
        return self.__dict__


class EntitasModel(LoggerMixin, SerializerMixin):
    def __init__(self, id_entitas: int, nama: str) -> None:
        self.id = id_entitas
        self.nama = nama

entitas = EntitasModel(1, "Produk A")
entitas.log("Data berhasil disimpan ke database.")
print(f"Serialized Dict: {entitas.to_dict()}")

# Melihat urutan pencarian method (MRO):
print(f"MRO Urutan Pencarian: {[cls.__name__ for cls in EntitasModel.mro()]}")


print("\n" + "=" * 70)
print("✅ KESIMPULAN & BEST PRACTICE FILE 01:")
print("1. Gunakan `@property` daripada getter/setter bergaya Java (contoh: `get_saldo()`).")
print("2. Awali nama atribut dengan single underscore `_` untuk penanda internal (protected).")
print("3. Gunakan `@classmethod` untuk pola Factory Method pembuatan objek alternatif.")
print("4. Manfaatkan `abc.ABC` untuk mendefinisikan antarmuka arsitektural yang konsisten.")
print("5. Mixin class harus bersifat stateless dan fokus pada satu tanggung jawab tambahan.")
print("=" * 70)
