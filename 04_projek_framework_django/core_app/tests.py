"""
Suite Pengujian Otomatis Django (Model, Views & REST API)
"""

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Kategori, Produk

class TestKatalogDjango(TestCase):
    def setUp(self):
        """Persiapan data awal untuk setiap pengujian."""
        self.kategori = Kategori.objects.create(
            nama="Elektronik",
            deskripsi="Perangkat gadget dan komputer"
        )
        self.produk1 = Produk.objects.create(
            kategori=self.kategori,
            nama="Laptop Pro 16",
            sku="LPT-001",
            harga=20000000.0,
            stok=5,
            aktif=True
        )
        self.produk_habis = Produk.objects.create(
            kategori=self.kategori,
            nama="Kabel Adapter Habis",
            sku="CBL-000",
            harga=50000.0,
            stok=0,
            aktif=True
        )
        self.client_web = Client()
        self.client_api = APIClient()

    def test_model_slug_otomatis(self):
        """Memastikan slug digenerate otomatis saat create."""
        self.assertEqual(self.kategori.slug, "elektronik")
        self.assertEqual(self.produk1.slug, "laptop-pro-16")

    def test_custom_manager_tersedia(self):
        """Memastikan manager .tersedia() hanya mengembalikan barang stok > 0."""
        produk_tersedia = Produk.objects.tersedia()
        self.assertEqual(produk_tersedia.count(), 1)
        self.assertIn(self.produk1, produk_tersedia)
        self.assertNotIn(self.produk_habis, produk_tersedia)

    def test_halaman_web_beranda(self):
        """Menguji apakah view HTML merespons dengan HTTP 200."""
        response = self.client_web.get(reverse('beranda_katalog'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Laptop Pro 16")

    def test_api_health_check(self):
        """Menguji status endpoint health check API."""
        response = self.client_api.get(reverse('api_health'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'HEALTHY')

    def test_api_get_produk_list(self):
        """Menguji pemanggilan GET /api/v1/produk/."""
        response = self.client_api.get(reverse('api_produk_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_api_post_produk_valid(self):
        """Menguji pembuatan produk baru via REST API."""
        payload = {
            "kategori": self.kategori.id,
            "nama": "Mouse Bluetooth Ergonomis",
            "sku": "MSE-999",
            "harga": 350000.0,
            "stok": 20,
            "aktif": True
        }
        response = self.client_api.post(reverse('api_produk_list'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['sku'], 'MSE-999')
        self.assertEqual(Produk.objects.count(), 3)

    def test_api_post_produk_sku_invalid(self):
        """Menguji penolakan validasi serializer jika SKU kependekan."""
        payload = {
            "kategori": self.kategori.id,
            "nama": "Item Gagal",
            "sku": "A",  # Minimal 3 karakter
            "harga": 10000.0,
            "stok": 5,
        }
        response = self.client_api.post(reverse('api_produk_list'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('sku', response.data)
