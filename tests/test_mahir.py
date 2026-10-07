"""
Unit Test Suite untuk Modul 03: Tingkat Mahir Python
"""

import unittest
import sys
import asyncio
from pathlib import Path
from importlib import import_module

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

mod_meta = import_module("03_mahir.01_metaprogramming_dan_descriptors")
mod_async = import_module("03_mahir.03_asynchronous_asyncio")
mod_typing = import_module("03_mahir.05_typing_sistem_lanjut")

class TestMahirPython(unittest.TestCase):

    def test_descriptor_validation(self):
        produk = mod_meta.ProdukModel("Headphone", 1_500_000, 10)
        self.assertEqual(produk.harga, 1_500_000)
        with self.assertRaises(ValueError):
            produk.harga = -500
        with self.assertRaises(TypeError):
            produk.stok = "sepuluh"

    def test_singleton_metaclass(self):
        inst1 = mod_meta.DatabasePool()
        inst2 = mod_meta.DatabasePool()
        self.assertIs(inst1, inst2)

    def test_protocol_structural_typing(self):
        task = mod_typing.TaskSistem()
        robot = mod_typing.RobotPembersih()
        self.assertTrue(isinstance(robot, mod_typing.DapatDirencanakan))
        self.assertIn("berjalan", task.eksekusi())
        self.assertIn("membersihkan", robot.eksekusi())

    def test_async_fetch(self):
        async def run_async():
            res = await mod_async.fetch_data("Unit-Test-API", 0.01)
            return res
        hasil = asyncio.run(run_async())
        self.assertEqual(hasil["sumber"], "Unit-Test-API")

if __name__ == "__main__":
    unittest.main()
