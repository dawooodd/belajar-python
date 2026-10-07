"""
Submodul Aritmatika: Menyediakan fungsi perhitungan aritmatika dasar.
"""

def tambah(a: float, b: float) -> float:
    """Menjumlahkan dua bilangan."""
    return a + b

def kali(a: float, b: float) -> float:
    """Mengalikan dua bilangan."""
    return a * b

def pangkat(basis: float, eksponen: float) -> float:
    """Memangkatkan basis dengan eksponen."""
    return basis ** eksponen

# Modul dapat diuji secara mandiri
if __name__ == "__main__":
    print(f"Uji Mandiri Aritmatika: 2^8 = {pangkat(2, 8)}")
