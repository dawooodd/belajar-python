"""
Form HTML Django untuk Manajemen Produk
"""

from django import forms
from .models import Produk

class ProdukForm(forms.ModelForm):
    class Meta:
        model = Produk
        fields = ["kategori", "nama", "sku", "harga", "stok", "aktif"]
        widgets = {
            "kategori": forms.Select(attrs={"class": "w-full p-2 border rounded-lg bg-gray-50 dark:bg-gray-700"}),
            "nama": forms.TextInput(attrs={"class": "w-full p-2 border rounded-lg", "placeholder": "Contoh: Laptop Gaming"}),
            "sku": forms.TextInput(attrs={"class": "w-full p-2 border rounded-lg", "placeholder": "SKU-990"}),
            "harga": forms.NumberInput(attrs={"class": "w-full p-2 border rounded-lg", "step": "1000"}),
            "stok": forms.NumberInput(attrs={"class": "w-full p-2 border rounded-lg"}),
            "aktif": forms.CheckboxInput(attrs={"class": "w-4 h-4 text-indigo-600 rounded"}),
        }
