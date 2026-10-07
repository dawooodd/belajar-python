"""
Views Fullstack (MVT - Model View Template) Django
Menampilkan halaman frontend katalog produk & formulir input data.
"""

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Produk, Kategori
from .forms import ProdukForm

class BerandaKatalogView(ListView):
    model = Produk
    template_name = "index.html"
    context_object_name = "daftar_produk"
    paginate_by = 6

    def get_queryset(self):
        # Menggunakan custom manager 'tersedia()'
        return Produk.objects.select_related("kategori").all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["daftar_kategori"] = Kategori.objects.all()
        context["form"] = ProdukForm()
        context["total_produk"] = Produk.objects.count()
        context["total_tersedia"] = Produk.objects.tersedia().count()
        return context

    def post(self, request, *args, **kwargs):
        """Menangani submit form tambah produk cepat."""
        form = ProdukForm(request.POST)
        if form.is_valid():
            produk_baru = form.save()
            messages.success(request, f"Produk '{produk_baru.nama}' berhasil ditambahkan!")
            return redirect("beranda_katalog")
        else:
            messages.error(request, "Gagal menyimpan: Periksa kembali formulir Anda.")
            self.object_list = self.get_queryset()
            context = self.get_context_data()
            context["form"] = form
            return render(request, self.template_name, context)
