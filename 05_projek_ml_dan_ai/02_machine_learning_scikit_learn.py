"""
================================================================================
MODUL 05: MACHINE LEARNING & ARTIFICIAL INTELLIGENCE (ML/AI)
FILE 02: End-to-End Machine Learning Pipeline dengan Scikit-Learn
================================================================================
Tujuan Pembelajaran:
1. Memahami siklus hidup Machine Learning: Data -> Preprocess -> Model -> Eval.
2. Membangun Pipeline anti-leakage dengan ColumnTransformer.
3. Melatih algoritma klasifikasi ensemble: Random Forest & Logistic Regression.
4. Hyperparameter tuning otomatis dengan GridSearchCV & Cross Validation.
5. Evaluasi metrik industri: ROC-AUC, F1-Score, Confusion Matrix.
6. Serialisasi model (joblib) dan pengujian inferensi data baru secara real-time.
================================================================================
"""

import numpy as np
import pandas as pd
from pathlib import Path
import joblib

from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

print("=" * 70)
print("🤖 MEMBANGUN PIPELINE MACHINE LEARNING SKALA PRODUKSI")
print("=" * 70)

# ------------------------------------------------------------------------------
# 1. Menyiapkan Dataset Sintetis Berstandar Real-World (Churn Prediction)
# ------------------------------------------------------------------------------
np.random.seed(42)
n_samples = 1000

umur = np.random.randint(18, 65, size=n_samples)
gaji_tahunan = np.random.uniform(30_000_000, 250_000_000, size=n_samples)
lama_berlangganan_bulan = np.random.randint(1, 72, size=n_samples)
tipe_paket = np.random.choice(["Basic", "Standard", "Premium"], size=n_samples, p=[0.5, 0.3, 0.2])
metode_bayar = np.random.choice(["Transfer", "KartuKredit", "EWallet"], size=n_samples)

# Probabilitas churn realistis: gaji rendah & jarang berlangganan -> churn lebih tinggi
skor_risiko = (
    (65 - umur) * 0.01 +
    (72 - lama_berlangganan_bulan) * 0.03 -
    (gaji_tahunan / 100_000_000) * 0.2 +
    (tipe_paket == "Basic") * 0.3
)
probabilitas_churn = 1 / (1 + np.exp(-skor_risiko))
target_churn = (np.random.rand(n_samples) < probabilitas_churn).astype(int)

df_churn = pd.DataFrame({
    "umur": umur,
    "gaji_tahunan": gaji_tahunan,
    "lama_berlangganan_bulan": lama_berlangganan_bulan,
    "tipe_paket": tipe_paket,
    "metode_bayar": metode_bayar,
    "churn": target_churn
})

print(f"Total Sampel : {len(df_churn)}")
print(f"Proporsi Churn: {df_churn['churn'].mean():.1%} churned, {1 - df_churn['churn'].mean():.1%} retained.")


# ------------------------------------------------------------------------------
# 2. Pemisahan Data (Train-Test Split)
# ------------------------------------------------------------------------------
X = df_churn.drop(columns=["churn"])
y = df_churn["churn"]

# Stratified split menjaga proporsi target seimbang di train dan test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"Ukuran Data Latih: {X_train.shape[0]} baris")
print(f"Ukuran Data Uji  : {X_test.shape[0]} baris")


# ------------------------------------------------------------------------------
# 3. Arsitektur Preprocessing: ColumnTransformer & Scikit-Learn Pipeline
# ------------------------------------------------------------------------------
fitur_numerik = ["umur", "gaji_tahunan", "lama_berlangganan_bulan"]
fitur_kategorik = ["tipe_paket", "metode_bayar"]

# Pipeline transformasi: scaling untuk numerik, one-hot encoding untuk kategorik
preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), fitur_numerik),
        ("cat", OneHotEncoder(drop="first", handle_unknown="ignore"), fitur_kategorik),
    ]
)

# Pipeline utuh: Preprocessor + Model Classifier
pipeline_rf = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(random_state=42))
    ]
)


# ------------------------------------------------------------------------------
# 4. Hyperparameter Tuning Otomatis (GridSearchCV)
# ------------------------------------------------------------------------------
print("\n--- [3] Menjalankan GridSearchCV & Cross Validation 3-Fold ---")

param_grid = {
    "classifier__n_estimators": [50, 100],
    "classifier__max_depth": [5, 10, None],
    "classifier__min_samples_split": [2, 5],
}

grid_search = GridSearchCV(
    pipeline_rf,
    param_grid,
    cv=3,
    scoring="f1",
    n_jobs=-1
)
grid_search.fit(X_train, y_train)

print(f"✅ Parameter Terbaik Ditemukan: {grid_search.best_params_}")
print(f"Skor F1 Validasi Silang Terbaik: {grid_search.best_score_:.4f}")

model_terbaik = grid_search.best_estimator_


# ------------------------------------------------------------------------------
# 5. Evaluasi Kinerja Model pada Data Uji (Unseen Test Set)
# ------------------------------------------------------------------------------
print("\n--- [4] Laporan Evaluasi Kinerja Model ---")

y_pred = model_terbaik.predict(X_test)
y_pred_proba = model_terbaik.predict_proba(X_test)[:, 1]

print("Classification Report:")
print(classification_report(y_test, y_pred, target_names=["Retain (0)", "Churn (1)"]))

auc_score = roc_auc_score(y_test, y_pred_proba)
print(f"Area Under ROC Curve (ROC-AUC): {auc_score:.4f}")

cm = confusion_matrix(y_test, y_pred)
print(f"Confusion Matrix:\n{cm}")


# ------------------------------------------------------------------------------
# 6. Serialisasi Model & Inferensi Real-Time
# ------------------------------------------------------------------------------
DIR_MODEL = Path(__file__).resolve().parent / "models_saved"
DIR_MODEL.mkdir(parents=True, exist_ok=True)
path_model_saved = DIR_MODEL / "churn_predictor_rf.joblib"

joblib.dump(model_terbaik, path_model_saved)
print(f"\n💾 Model berhasil diekspor ke: {path_model_saved.name}")

# Simulasi Inferensi Data Baru:
print("\n--- [5] Simulasi Prediksi Data Pelanggan Baru Masuk ---")
model_dimuat = joblib.load(path_model_saved)

pelanggan_baru = pd.DataFrame([{
    "umur": 22,
    "gaji_tahunan": 35_000_000.0,
    "lama_berlangganan_bulan": 2,
    "tipe_paket": "Basic",
    "metode_bayar": "Transfer"
}])

prediksi_kelas = model_dimuat.predict(pelanggan_baru)[0]
peluang_churn = model_dimuat.predict_proba(pelanggan_baru)[0, 1]

print(f"Data Input: {pelanggan_baru.to_dict(orient='records')[0]}")
print(f"Hasil Analisis: {'🚨 Berisiko Tinggi Churn!' if prediksi_kelas == 1 else '✅ Pelanggan Loyal'}")
print(f"Probabilitas Churn: {peluang_churn:.1%}")


print("\n" + "=" * 70)
print("✅ KESIMPULAN & BEST PRACTICE FILE 02 (ML/AI):")
print("1. Selalu gunakan `sklearn.pipeline.Pipeline` untuk mencegah Data Leakage saat transformasi.")
print("2. Gunakan metrik F1-Score atau ROC-AUC daripada Accuracy jika dataset tidak seimbang (imbalanced).")
print("3. Simpan seluruh pipeline (bukan hanya model klasifikasi) agar preprocessing dapat langsung diaplikasikan pada inferensi produksi.")
print("=" * 70)
