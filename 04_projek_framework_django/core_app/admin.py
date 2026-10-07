"""
Konfigurasi Panel Admin Django
"""

from django.contrib import admin
from .models import Kategori, Produk

@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    list_display = ["id", "nama", "slug", "dibuat_pada"]
    prepopulated_fields = {"slug": ("nama",)}
    search_fields = ["nama"]


@admin.register(Produk)
class ProdukAdmin(admin.ModelAdmin):
    list_display = ["id", "nama", "sku", "kategori", "harga", "stok", "aktif", "dibuat_pada"]
    list_filter = ["aktif", "kategori", "dibuat_pada"]
    search_fields = ["nama", "sku"]
    prepopulated_fields = {"slug": ("nama",)}
    list_editable = ["harga", "stok", "aktif"]
