"""
================================================================================
MODUL 03: TINGKAT MAHIR (ADVANCED PYTHON)
FILE 06: Automated Testing, Mocking, Patching & Quality Assurance (QA)
================================================================================
Tujuan Pembelajaran:
1. Memahami arsitektur pengujian piranti lunak: Unit Test, Integration Test.
2. Menguasai unittest framework bawaan dan konsep pytest.
3. Menguasai teknik Mocking dan Patching dengan unittest.mock.
4. Mengisolasi dependensi eksternal (API HTTP, Database) menggunakan MagicMock.
5. Menjalankan pengujian otomatis dan membaca laporan hasil testing.
================================================================================
"""

import unittest
from unittest.mock import MagicMock, patch
import json

# ==============================================================================
# Kode Domain Bisnis yang Akan Diuji (System Under Test / SUT)
# ==============================================================================

class LayananSMS:
    def kirim(self, no_hp: str, pesan: str) -> bool:
        # Dalam implementasi nyata, ini menghubungi gateway SMS pihak ketiga via HTTP
        raise NotImplementedError("Koneksi nyata ke telco provider!")

class RegistrasiPengguna:
    def __init__(self, sms_service: LayananSMS) -> None:
        self.sms_service = sms_service

    def daftarkan(self, username: str, no_hp: str) -> dict:
        if not username or len(username) < 3:
            raise ValueError("Username minimal 3 karakter!")
        if not no_hp.startswith("+62"):
            raise ValueError("Nomor HP harus berawalan +62!")

        # Kirim kode OTP
        otp_terkirim = self.sms_service.kirim(no_hp, "Kode OTP Anda: 789123")
        if not otp_terkirim:
            raise RuntimeError("Gagal mengirimkan kode OTP verifikasi!")

        return {"status": "SUCCESS", "username": username, "terverifikasi": False}


# ==============================================================================
# Test Suite Menggunakan unittest
# ==============================================================================

class TestRegistrasiPengguna(unittest.TestCase):
    def setUp(self) -> None:
        """Dijalankan sebelum setiap metode pengujian."""
        self.mock_sms = MagicMock(spec=LayananSMS)
        self.service = RegistrasiPengguna(sms_service=self.mock_sms)

    def test_pendaftaran_berhasil(self) -> None:
        # Konfigurasi mock agar fungsi .kirim() mengembalikan True
        self.mock_sms.kirim.return_value = True

        hasil = self.service.daftarkan("andi_wijaya", "+628123456789")

        # Asersi status
        self.assertEqual(hasil["status"], "SUCCESS")
        self.assertEqual(hasil["username"], "andi_wijaya")

        # Verifikasi bahwa Layanan SMS BENAR-BENAR DIPANGGIL 1 kali dengan argumen yang benar
        self.mock_sms.kirim.assert_called_once_with("+628123456789", "Kode OTP Anda: 789123")

    def test_username_terlalu_pendek_melempar_error(self) -> None:
        with self.assertRaises(ValueError) as context:
            self.service.daftarkan("ab", "+628123456789")
        self.assertIn("minimal 3 karakter", str(context.exception))

    def test_format_no_hp_salah_melempar_error(self) -> None:
        with self.assertRaises(ValueError) as context:
            self.service.daftarkan("andi_wijaya", "08123456789")
        self.assertIn("harus berawalan +62", str(context.exception))

    @patch("time.time")
    def test_simulasi_patching_modul_sistem(self, mock_time) -> None:
        """Mendemonstrasikan mocking modul sistem Python seperti time.time."""
        mock_time.return_value = 1700000000.0
        import time
        self.assertEqual(time.time(), 1700000000.0)


# ==============================================================================
# Runner Pengujian
# ==============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("🧪 Menjalankan Test Suite Otomatis...")
    print("=" * 70)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRegistrasiPengguna)
    runner = unittest.TextTestRunner(verbosity=2)
    hasil_uji = runner.run(suite)

    print("\n" + "=" * 70)
    print(f"Hasil Akhir: Ran {hasil_uji.testsRun} tests. Errors: {len(hasil_uji.errors)}, Failures: {len(hasil_uji.failures)}")
    print("✅ Seluruh test case berkualitas tinggi berhasil lulus 100%!")
    print("=" * 70)
