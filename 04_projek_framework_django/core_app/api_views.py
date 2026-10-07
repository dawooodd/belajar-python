"""
REST API Endpoints menggunakan Django REST Framework (DRF)
Menyediakan operasi CRUD lengkap via HTTP (GET, POST, PUT, DELETE).
"""

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Produk, Kategori
from .serializers import ProdukSerializer, KategoriSerializer

class KategoriListCreateAPIView(generics.ListCreateAPIView):
    """
    GET  /api/v1/kategori/  -> Mengambil daftar semua kategori
    POST /api/v1/kategori/  -> Membuat kategori baru
    """
    queryset = Kategori.objects.all()
    serializer_class = KategoriSerializer


class ProdukListCreateAPIView(generics.ListCreateAPIView):
    """
    GET  /api/v1/produk/  -> Mengambil daftar produk (dengan filter kategori & pencarian)
    POST /api/v1/produk/  -> Mendaftarkan produk baru
    """
    serializer_class = ProdukSerializer

    def get_queryset(self):
        queryset = Produk.objects.select_related("kategori").all()
        kategori_id = self.request.query_params.get("kategori")
        hanya_tersedia = self.request.query_params.get("tersedia")
        
        if kategori_id:
            queryset = queryset.filter(kategori_id=kategori_id)
        if hanya_tersedia == "true":
            queryset = queryset.tersedia()
        return queryset


class ProdukDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/v1/produk/<id>/ -> Detail produk
    PUT    /api/v1/produk/<id>/ -> Update seluruh field
    PATCH  /api/v1/produk/<id>/ -> Update sebagian field
    DELETE /api/v1/produk/<id>/ -> Hapus produk
    """
    queryset = Produk.objects.all()
    serializer_class = ProdukSerializer
    lookup_field = "id"


class APIHealthCheckView(APIView):
    """Endpoint diagnosa kesehatan backend server."""
    def get(self, request):
        return Response({
            "status": "HEALTHY",
            "framework": "Django 5.x + Django REST Framework",
            "database": "SQLite (Development) / PostgreSQL Ready",
            "total_produk": Produk.objects.count()
        }, status=status.HTTP_200_OK)
