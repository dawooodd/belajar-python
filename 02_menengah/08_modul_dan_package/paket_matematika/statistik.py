"""
Submodul Statistik: Menyediakan fungsi statistik deskriptif.
"""

import math
from typing import Sequence

def hitung_rata_rata(data: Sequence[float]) -> float:
    """Menghitung nilai rata-rata (mean)."""
    if not data:
        raise ValueError("Data tidak boleh kosong!")
    return sum(data) / len(data)

def hitung_median(data: Sequence[float]) -> float:
    """Menghitung nilai tengah (median)."""
    if not data:
        raise ValueError("Data tidak boleh kosong!")
    data_urut = sorted(data)
    n = len(data_urut)
    tengah = n // 2
    if n % 2 == 1:
        return float(data_urut[tengah])
    return (data_urut[tengah - 1] + data_urut[tengah]) / 2.0

def hitung_standar_deviasi(data: Sequence[float]) -> float:
    """Menghitung standar deviasi sampel."""
    if len(data) < 2:
        raise ValueError("Standar deviasi butuh minimal 2 data poin!")
    mean = hitung_rata_rata(data)
    varians = sum((x - mean) ** 2 for x in data) / (len(data) - 1)
    return math.sqrt(varians)
