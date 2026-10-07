"""
================================================================================
MASTER TEST RUNNER: Belajar Python (Dasar -> Menengah -> Mahir -> Django -> ML/AI)
================================================================================
Menjalankan pengujian otomatis end-to-end pada seluruh modul kurikulum.
================================================================================
"""

import sys
import os
import unittest
import subprocess
from pathlib import Path

# Proteksi encoding UTF-8 untuk terminal Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(__file__).resolve().parent

def jalankan_master_suite():
    print("=" * 80)
    print("🧪 MEMULAI MASTER TEST SUITE: EVALUASI LINTAS MODUL KURIKULUM PYTHON")
    print("=" * 80)

    # 1. Menjalankan Unit Tests (Dasar, Menengah, Mahir)
    print("\n[FASE 1/3] Menjalankan Unit Test Modul Dasar, Menengah, dan Mahir...")
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    from tests.test_dasar import TestDasarPython
    from tests.test_menengah import TestMenengahPython
    from tests.test_mahir import TestMahirPython

    suite.addTests(loader.loadTestsFromTestCase(TestDasarPython))
    suite.addTests(loader.loadTestsFromTestCase(TestMenengahPython))
    suite.addTests(loader.loadTestsFromTestCase(TestMahirPython))

    runner = unittest.TextTestRunner(verbosity=2)
    hasil_core = runner.run(suite)

    # 2. Menjalankan Test Django
    print("\n[FASE 2/3] Menjalankan Test Suite Framework Django (Model, Views & REST API)...")
    cmd_django = [sys.executable, "manage.py", "test"]
    cwd_django = ROOT_DIR / "04_projek_framework_django"
    res_django = subprocess.run(cmd_django, cwd=cwd_django, capture_output=True, text=True, encoding="utf-8")
    
    if res_django.returncode == 0:
        print("✅ Seluruh 7 Test Case Django & DRF BERHASIL LULUS 100%!")
    else:
        print("❌ Django Test Mengalami Kendala:")
        print(res_django.stderr or res_django.stdout)

    # 3. Menjalankan Test Pipeline ML & AI
    print("\n[FASE 3/3] Menjalankan Integration Test Pipeline ML, PyTorch & AI Agent...")
    cmd_ml = [sys.executable, "test_ml_ai_pipeline.py"]
    cwd_ml = ROOT_DIR / "05_projek_ml_dan_ai"
    res_ml = subprocess.run(cmd_ml, cwd=cwd_ml, capture_output=True, text=True, encoding="utf-8")

    if res_ml.returncode == 0:
        print("✅ Seluruh 5 Test Case NumPy, Pandas, Scikit-learn, PyTorch & AI BERHASIL LULUS 100%!")
    else:
        print("❌ ML/AI Test Mengalami Kendala:")
        print(res_ml.stderr or res_ml.stdout)

    # Ringkasan Akhir
    print("\n" + "=" * 80)
    total_lulus = hasil_core.wasSuccessful() and (res_django.returncode == 0) and (res_ml.returncode == 0)
    if total_lulus:
        print("🎉 STATUS KURIKULUM: 100% ALL TESTS PASSING! SEMPURNA!")
        print("Kurikulum siap digunakan untuk pembelajaran mandiri, tim, dan portfolio!")
    else:
        print("⚠️ Terdapat modul yang membutuhkan peninjauan.")
    print("=" * 80)

if __name__ == "__main__":
    jalankan_master_suite()
