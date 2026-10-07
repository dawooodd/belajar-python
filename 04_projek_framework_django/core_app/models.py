"""
Model Database Relasional untuk Aplikasi Katalog & Inventori
Menggunakan Django ORM, Custom Managers, dan Validasi Model.
"""

from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator

class Kategori(models.Model):
    nama = models.CharField(max_length=100, unique=True, verbose_name="Nama Kategori")
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    deskripsi = models.TextField(blank=True, verbose_name="Deskripsi")
    dibuat_pada = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Kategori"
        ordering = ["nama"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nama)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.nama


class ProdukQuerySet(models.QuerySet):
    """Custom QuerySet untuk query chaining yang ekspresif."""
    def aktif(self):
        return self.filter(aktif=True)

    def tersedia(self):
        return self.filter(aktif=True, stok__gt=0)


class ProdukManager(models.Manager):
    def get_queryset(self):
        return ProdukQuerySet(self.model, using=self._db)

    def tersedia(self):
        return self.get_queryset().tersedia()


class Produk(models.Model):
    kategori = models.ForeignKey(
        Kategori,
        on_delete=models.CASCADE,
        related_name="produk",
        verbose_name="Kategori Induk"
    )
    nama = models.CharField(max_length=200, verbose_name="Nama Produk")
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    sku = models.CharField(max_length=50, unique=True, verbose_name="Kode SKU")
    harga = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.0)],
        verbose_name="Harga (Rp)"
    )
    stok = models.PositiveIntegerField(default=0, verbose_name="Jumlah Stok")
    aktif = models.BooleanField(default=True, verbose_name="Status Aktif")
    dibuat_pada = models.DateTimeField(auto_now_add=True)
    diperbarui_pada = models.DateTimeField(auto_now=True)

    # Manager kustom
    objects = ProdukManager()

    class Meta:
        ordering = ["-dibuat_pada"]
        indexes = [
            models.Index(fields=["sku"]),
            models.Index(fields=["slug"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nama)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.nama} ({self.sku}) - Rp {self.harga:,.2f}"
