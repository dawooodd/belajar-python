"""
Routing URL Aplikasi core_app (HTML Web & JSON REST API)
"""

from django.urls import path
from .views import BerandaKatalogView
from .api_views import (
    KategoriListCreateAPIView,
    ProdukListCreateAPIView,
    ProdukDetailAPIView,
    APIHealthCheckView,
)

urlpatterns = [
    # Web Front-end (MVT)
    path('', BerandaKatalogView.as_view(), name='beranda_katalog'),

    # REST API Endpoints (v1)
    path('api/v1/health/', APIHealthCheckView.as_view(), name='api_health'),
    path('api/v1/kategori/', KategoriListCreateAPIView.as_view(), name='api_kategori_list'),
    path('api/v1/produk/', ProdukListCreateAPIView.as_view(), name='api_produk_list'),
    path('api/v1/produk/<int:id>/', ProdukDetailAPIView.as_view(), name='api_produk_detail'),
]
