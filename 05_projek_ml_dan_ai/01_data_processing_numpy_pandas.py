"""
================================================================================
MODUL 05: MACHINE LEARNING & ARTIFICIAL INTELLIGENCE (ML/AI)
FILE 01: Manipulasi Data Numerik & Analisis Data Eksploratif (NumPy & Pandas)
================================================================================
Tujuan Pembelajaran:
1. Memahami NumPy Array (ndarray), Vektorisasi, dan Broadcasting.
2. Operasi Aljabar Linier (Dot Product, Matriks Perkalian @).
3. Pembersihan Data dengan Pandas DataFrame (Missing Values, Outliers).
4. Manipulasi Lanjutan: loc vs iloc, GroupBy, Agregasi, dan Feature Engineering.
5. Menyiapkan dataset bersih untuk pemodelan Machine Learning.
================================================================================
"""

import numpy as np
import pandas as pd
from pathlib import Path

print("=" * 70)
print(f"📊 NumPy Versi : {np.__version__}")
print(f"🐼 Pandas Versi: {pd.__version__}")
print("=" * 70)


# ------------------------------------------------------------------------------
# 1. NumPy: Vektorisasi & Broadcasting
# ------------------------------------------------------------------------------
print("\n--- [1] NumPy: Kecepatan Vektorisasi & Broadcasting ---")

# Vektorisasi vs Python Loop (Vektorisasi berjalan di level bahasa C tanpa overhead)
vektor_a = np.array([1.5, 2.0, 3.5, 4.0])
vektor_b = np.array([10.0, 20.0, 30.0, 40.0])

penjumlahan_vektor = vektor_a + vektor_b
perkalian_vektor = vektor_a * 2.5  # Broadcasting: skalar 2.5 disebarkan ke semua elemen

print(f"Vektor A       : {vektor_a}")
print(f"Vektor B       : {vektor_b}")
print(f"A + B (Vektor) : {penjumlahan_vektor}")
print(f"A * 2.5 (Broad): {perkalian_vektor}")

# Aljabar Linier: Matriks Perkalian (@)
matriks_1 = np.array([[1, 2], [3, 4]])
matriks_2 = np.array([[5, 6], [7, 8]])
hasil_dot = matriks_1 @ matriks_2  # Setara np.matmul()

print(f"\nMatriks Perkalian (Dot Product @):\n{hasil_dot}")
print(f"Determinan matriks 1: {np.linalg.det(matriks_1):.2f}")


# ------------------------------------------------------------------------------
# 2. Pandas: Data Ingestion & Data Wrangling
# ------------------------------------------------------------------------------
print("\n--- [2] Pandas: Pembuatan & Pembersihan Dataset Pelanggan ---")

# Simulasi dataset transaksi e-commerce
data_mentah = {
    "id_pelanggan": [101, 102, 103, 104, 105, 106, 107, 108],
    "umur": [24, 35, np.nan, 45, 29, 52, np.nan, 31],
    "kota": ["Jakarta", "Surabaya", "Bandung", "Jakarta", "Surabaya", "Medan", "Jakarta", "Bandung"],
    "total_belanja_juta": [2.5, 12.0, 4.8, 18.5, 3.2, 25.0, 1.2, 8.5],
    "frekuensi_kunjungan": [5, 22, 9, 30, 7, 45, 2, 14],
    "status_churn": [0, 0, 1, 0, 1, 0, 1, 0]  # 1 = Berhenti belanja, 0 = Masih aktif
}

df = pd.DataFrame(data_mentah)
print("Data Mentah Awal:")
print(df.head(4))

# Analisis Missing Values (Nilai Kosong)
print(f"\nMissing values per kolom:\n{df.isna().sum()}")

# Imputasi Nilai Kosong: Mengisi umur dengan nilai Median kota atau median global
median_umur = df["umur"].median()
df["umur"] = df["umur"].fillna(median_umur)
print(f"Imputasi umur dengan median ({median_umur} tahun) selesai.")


# ------------------------------------------------------------------------------
# 3. Feature Engineering: Menciptakan Fitur Baru yang Bermanfaat
# ------------------------------------------------------------------------------
print("\n--- [3] Feature Engineering ---")

# Menghitung rata-rata belanja per kunjungan
df["rata_rata_per_kunjungan"] = df["total_belanja_juta"] / df["frekuensi_kunjungan"]

# Segmentasi pelanggan berbasis kuartil belanja
df["kategori_belanja"] = pd.qcut(
    df["total_belanja_juta"],
    q=3,
    labels=["Bronze", "Silver", "Gold"]
)

print(df[["id_pelanggan", "total_belanja_juta", "rata_rata_per_kunjungan", "kategori_belanja"]].head(5))


# ------------------------------------------------------------------------------
# 4. Agregasi & Analisis GroupBy
# ------------------------------------------------------------------------------
print("\n--- [4] Agregasi GroupBy Berbasis Kota ---")

ringkasan_kota = df.groupby("kota").agg(
    total_pelanggan=("id_pelanggan", "count"),
    rata_rata_belanja=("total_belanja_juta", "mean"),
    total_omset=("total_belanja_juta", "sum"),
    tingkat_churn=("status_churn", "mean")
).reset_index()

# Urutkan berdasarkan total omset tertinggi
ringkasan_kota = ringkasan_kota.sort_values(by="total_omset", ascending=False)
print(ringkasan_kota)


# ------------------------------------------------------------------------------
# 5. Export Dataset yang Sudah Bersih
# ------------------------------------------------------------------------------
DIR_OUTPUT = Path(__file__).resolve().parent / "data_clean"
DIR_OUTPUT.mkdir(parents=True, exist_ok=True)
path_csv_bersih = DIR_OUTPUT / "dataset_pelanggan_bersih.csv"

df.to_csv(path_csv_bersih, index=False)
print(f"\n✅ Dataset bersih berhasil disimpan ke: {path_csv_bersih.name}")


print("\n" + "=" * 70)
print("✅ KESIMPULAN & BEST PRACTICE FILE 01 (ML/AI):")
print("1. Gunakan array NumPy daripada Python list untuk operasi numerik karena efisiensi memori C-contiguous.")
print("2. Hindari loop 'for' saat menghitung kolom Pandas — selalu gunakan operasi vectorized.")
print("3. Periksa missing values secara teliti dan gunakan median/modus alih-alih drop jika data berharga.")
print("4. Feature engineering yang tepat menyumbang >70% keberhasilan model Machine Learning.")
print("=" * 70)
