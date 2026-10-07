"""
Unit Test Suite untuk Modul 01: Dasar Pemrograman Python
"""

import unittest
import sys
from pathlib import Path

# Menambahkan root project ke sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Import fungsi latihan dari modul 01
from importlib import import_module
latihan_dasar = import_module("01_dasar.07_latihan_dasar")

class TestDasarPython(unittest.TestCase):

    def test_palindrom(self):
        self.assertTrue(latihan_dasar.is_palindrom("Kasur ini rusak"))
        self.assertTrue(latihan_dasar.is_palindrom("Madam, I'm Adam"))
        self.assertFalse(latihan_dasar.is_palindrom("Python Programming"))

    def test_group_anagrams(self):
        kata_list = ["eat", "tea", "tan", "ate", "nat", "bat"]
        kelompok = latihan_dasar.group_anagrams(kata_list)
        self.assertEqual(len(kelompok), 3)

    def test_two_sum(self):
        nums = [2, 7, 11, 15]
        target = 9
        hasil = latihan_dasar.two_sum(nums, target)
        self.assertEqual(hasil, (0, 1))

    def test_kompresi_string(self):
        self.assertEqual(latihan_dasar.kompresi_string("aabcccccaaa"), "a2b1c5a3")
        self.assertEqual(latihan_dasar.kompresi_string("abc"), "abc")

    def test_putar_matriks_90(self):
        m = [[1, 2], [3, 4]]
        hasil = latihan_dasar.putar_matriks_90(m)
        self.assertEqual(hasil, [[3, 1], [4, 2]])

if __name__ == "__main__":
    unittest.main()
