"""
Unit Test Suite untuk Modul 02: Tingkat Menengah Python
"""

import unittest
import sys
from pathlib import Path
from importlib import import_module

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Dynamic imports untuk modul dengan awalan angka
mod_oop = import_module("02_menengah.01_oop_dasar_ke_lanjut")
mod_dunder = import_module("02_menengah.02_dunder_dan_magic_methods")
mod_data = import_module("02_menengah.03_dataclasses_dan_pydantic")
sys.path.insert(0, str(ROOT_DIR / "02_menengah" / "08_modul_dan_package"))
import paket_matematika

class TestMenengahPython(unittest.TestCase):

    def test_oop_rekening_bank(self):
        rek = mod_oop.RekeningBank("User A", 100_000.0)
        self.assertEqual(rek.saldo, 100_000.0)
        rek.setor(50_000.0)
        self.assertEqual(rek.saldo, 150_000.0)
        self.assertTrue(rek.tarik(70_000.0))
        self.assertEqual(rek.saldo, 80_000.0)
        with self.assertRaises(ValueError):
            rek.saldo = -100

    def test_dunder_vektor_2d(self):
        v1 = mod_dunder.Vektor2D(3, 4)
        v2 = mod_dunder.Vektor2D(1, 2)
        v_sum = v1 + v2
        self.assertEqual(v_sum.x, 4.0)
        self.assertEqual(v_sum.y, 6.0)
        self.assertEqual(abs(v1), 5.0)

    def test_dataclass_pesanan_ordering(self):
        i1 = mod_data.ItemPesanan("Barang Murah", 10_000, 1)
        i2 = mod_data.ItemPesanan("Barang Mahal", 50_000, 2)
        self.assertTrue(i1 < i2)

    def test_paket_matematika(self):
        self.assertEqual(paket_matematika.tambah(10, 5), 15)
        self.assertEqual(paket_matematika.pangkat(2, 4), 16)
        data = [10.0, 20.0, 30.0]
        self.assertEqual(paket_matematika.hitung_rata_rata(data), 20.0)
        self.assertEqual(paket_matematika.hitung_median(data), 20.0)

if __name__ == "__main__":
    unittest.main()
