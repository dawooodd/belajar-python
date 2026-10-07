"""
Inisialisasi Package Matematika
Mengekspos API publik dengan mendefinisikan __all__
"""

from .aritmatika import tambah, kali, pangkat
from .statistik import hitung_rata_rata, hitung_median, hitung_standar_deviasi

__all__ = [
    "tambah",
    "kali",
    "pangkat",
    "hitung_rata_rata",
    "hitung_median",
    "hitung_standar_deviasi",
]

VERSI_PAKET = "1.0.0"
