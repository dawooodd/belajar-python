"""
Serializers untuk Django REST Framework (DRF)
Menangani konversi Model ke JSON dan validasi request masuk.
"""

from rest_framework import serializers
from .models import Kategori, Produk

class KategoriSerializer(serializers.ModelSerializer):
    total_produk = serializers.IntegerField(source="produk.count", read_only=True)

    class Meta:
        model = Kategori
        fields = ["id", "nama", "slug", "deskripsi", "total_produk", "dibuat_pada"]
        read_only_fields = ["slug", "dibuat_pada"]


class ProdukSerializer(serializers.ModelSerializer):
    kategori_nama = serializers.CharField(source="kategori.nama", read_only=True)

    class Meta:
        model = Produk
        fields = [
            "id",
            "kategori",
            "kategori_nama",
            "nama",
            "slug",
            "sku",
            "harga",
            "stok",
            "aktif",
            "dibuat_pada",
            "diperbarui_pada"
        ]
        read_only_fields = ["slug", "dibuat_pada", "diperbarui_pada"]

    def validate_sku(self, value: str) -> str:
        """Validasi kustom memastikan SKU berupa uppercase tanpa spasi."""
        cleaned_sku = value.strip().upper()
        if len(cleaned_sku) < 3:
            raise serializers.ValidationError("SKU minimal 3 karakter!")
        return cleaned_sku

    def validate_harga(self, value: float) -> float:
        if value <= 0:
            raise serializers.ValidationError("Harga produk harus lebih dari 0!")
        return value
