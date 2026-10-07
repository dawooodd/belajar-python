"""
================================================================================
MODUL 05: MACHINE LEARNING & ARTIFICIAL INTELLIGENCE (ML/AI)
FILE 03: Deep Learning Fundamental & Neural Networks dengan PyTorch
================================================================================
Tujuan Pembelajaran:
1. Memahami Tensor PyTorch, Operasi Matriks, dan Autograd Engine (Automatic Differentiation).
2. Memilih Device Akselerasi secara adaptif (CUDA GPU vs CPU).
3. Merancang Arsitektur Jaringan Saraf Tiruan (Deep Neural Network) via torch.nn.Module.
4. Mengimplementasikan torch.utils.data.Dataset dan DataLoader untuk batching.
5. Menulis Siklus Pelatihan Lengkap (Training & Validation Loop):
   - Forward Pass, Loss Function, Backpropagation, Optimizer Step.
6. Menyimpan & memuat state weights model (torch.save/load state_dict).
================================================================================
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from pathlib import Path
import numpy as np

print("=" * 70)
print(f"🔥 PyTorch Versi: {torch.__version__}")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"🚀 Device Terdeteksi: {device} ({'GPU CUDA Aktif' if device.type == 'cuda' else 'CPU Mode Aktif'})")
print("=" * 70)


# ------------------------------------------------------------------------------
# 1. Tensor PyTorch & Autograd Engine (Diferensiasi Otomatis)
# ------------------------------------------------------------------------------
print("\n--- [1] Autograd Engine: Kalkulasi Gradien Otomatis ---")

# Misalkan fungsi: y = 3*x^2 + 2*x + 1
# Turunan dy/dx = 6*x + 2
# Pada x = 4.0 -> dy/dx = 6(4) + 2 = 26.0

x = torch.tensor([4.0], requires_grad=True)
y = 3 * (x ** 2) + 2 * x + 1

y.backward() # Menghitung gradien secara otomatis (backprop)
print(f"Input x: {x.item()}")
print(f"Hasil y: {y.item()}")
print(f"Gradien dy/dx otomatis dihitung oleh Autograd: {x.grad.item()} (Kalkulasi manual: 26.0)")


# ------------------------------------------------------------------------------
# 2. Custom Dataset & DataLoader
# ------------------------------------------------------------------------------
print("\n--- [2] Menyiapkan Dataset & PyTorch DataLoader ---")

class DatasetKlasifikasiSintetis(Dataset):
    def __init__(self, n_sampel: int = 1200) -> None:
        np.random.seed(42)
        # 4 Fitur input
        self.X = np.random.randn(n_sampel, 4).astype(np.float32)
        # Target: 3 Kelas (0, 1, 2) berdasarkan kombinasi fitur
        skor = self.X[:, 0] * 1.5 - self.X[:, 1] * 2.0 + self.X[:, 2] * 0.8
        self.y = np.zeros(n_sampel, dtype=np.int64)
        self.y[skor > 0.5] = 1
        self.y[skor > 1.8] = 2

    def __len__(self) -> int:
        return len(self.X)

    def __getitem__(self, idx: int) -> tuple[torch.Tensor, torch.Tensor]:
        return torch.from_numpy(self.X[idx]), torch.tensor(self.y[idx], dtype=torch.long)

dataset_penuh = DatasetKlasifikasiSintetis()
ukuran_latih = int(0.8 * len(dataset_penuh))
ukuran_val = len(dataset_penuh) - ukuran_latih

dataset_latih, dataset_val = torch.utils.data.random_split(dataset_penuh, [ukuran_latih, ukuran_val])

loader_latih = DataLoader(dataset_latih, batch_size=32, shuffle=True)
loader_val = DataLoader(dataset_val, batch_size=32, shuffle=False)

print(f"Data Latih: {len(dataset_latih)} sampel, Data Validasi: {len(dataset_val)} sampel.")


# ------------------------------------------------------------------------------
# 3. Arsitektur Deep Neural Network (nn.Module)
# ------------------------------------------------------------------------------
print("\n--- [3] Merancang Arsitektur Neural Network (nn.Module) ---")

class ModelJaringanSarafDalam(nn.Module):
    def __init__(self, dimensi_input: int = 4, hidden_units: int = 64, jumlah_kelas: int = 3) -> None:
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(dimensi_input, hidden_units),
            nn.BatchNorm1d(hidden_units),
            nn.ReLU(),
            nn.Dropout(p=0.2),  # Regularisasi untuk mencegah overfitting

            nn.Linear(hidden_units, hidden_units // 2),
            nn.ReLU(),

            nn.Linear(hidden_units // 2, jumlah_kelas)  # Output logits
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x)

model = ModelJaringanSarafDalam().to(device)
print("Struktur Arsitektur Model:\n", model)


# ------------------------------------------------------------------------------
# 4. Loop Pelatihan & Validasi Lengkap (Training Loop)
# ------------------------------------------------------------------------------
print("\n--- [4] Memulai Siklus Pelatihan (Epochs) ---")

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.005, weight_decay=1e-4)

EPOCHS = 10

for epoch in range(1, EPOCHS + 1):
    # Mode Pelatihan
    model.train()
    total_loss_latih = 0.0
    benar_latih = 0
    total_latih = 0

    for batch_X, batch_y in loader_latih:
        batch_X, batch_y = batch_X.to(device), batch_y.to(device)

        optimizer.zero_grad()            # 1. Reset gradien sebelumnya
        prediksi_logits = model(batch_X) # 2. Forward pass
        loss = criterion(prediksi_logits, batch_y) # 3. Hitung Loss
        loss.backward()                  # 4. Backpropagation
        optimizer.step()                 # 5. Update weights

        total_loss_latih += loss.item() * batch_X.size(0)
        _, pred_kelas = torch.max(prediksi_logits, 1)
        benar_latih += (pred_kelas == batch_y).sum().item()
        total_latih += batch_y.size(0)

    rata_loss_latih = total_loss_latih / total_latih
    akurasi_latih = benar_latih / total_latih

    # Mode Evaluasi / Validasi
    model.eval()
    total_loss_val = 0.0
    benar_val = 0
    total_val = 0

    with torch.no_grad():  # Matikan kalkulasi gradien untuk menghemat RAM & akselerasi
        for val_X, val_y in loader_val:
            val_X, val_y = val_X.to(device), val_y.to(device)
            logits_val = model(val_X)
            loss_v = criterion(logits_val, val_y)

            total_loss_val += loss_v.item() * val_X.size(0)
            _, pred_val = torch.max(logits_val, 1)
            benar_val += (pred_val == val_y).sum().item()
            total_val += val_y.size(0)

    akurasi_val = benar_val / total_val

    if epoch % 2 == 0 or epoch == EPOCHS:
        print(f"Epoch [{epoch:02d}/{EPOCHS:02d}] -> "
              f"Loss Latih: {rata_loss_latih:.4f} | Akurasi Latih: {akurasi_latih:.1%} | "
              f"Akurasi Validasi: {akurasi_val:.1%}")


# ------------------------------------------------------------------------------
# 5. Menyimpan Model Checkpoint & Inferensi
# ------------------------------------------------------------------------------
DIR_MODELS = Path(__file__).resolve().parent / "models_saved"
DIR_MODELS.mkdir(parents=True, exist_ok=True)
path_checkpoint = DIR_MODELS / "deep_classifier.pt"

torch.save(model.state_dict(), path_checkpoint)
print(f"\n💾 Model Weights berhasil disimpan ke: {path_checkpoint.name}")

# Inferensi sampel baru
model.eval()
sampel_baru = torch.tensor([[1.2, -0.8, 0.4, 0.1]], dtype=torch.float32).to(device)
with torch.no_grad():
    output_logits = model(sampel_baru)
    probabilitas = torch.softmax(output_logits, dim=1)
    kelas_terpilih = torch.argmax(probabilitas, dim=1).item()

print(f"\nInferensi Data Uji Baru:")
print(f"Logits          : {output_logits.cpu().numpy()}")
print(f"Probabilitas (%) : {probabilitas.cpu().numpy() * 100}")
print(f"Kelas Terprediksi: Kelas {kelas_terpilih}")


print("\n" + "=" * 70)
print("✅ KESIMPULAN & BEST PRACTICE FILE 03 (DEEP LEARNING):")
print("1. Selalu bersihkan gradien dengan `optimizer.zero_grad()` sebelum `loss.backward()`.")
print("2. Gunakan `with torch.no_grad():` dan `model.eval()` saat inferensi / validasi.")
print("3. Pindahkan tensors dan model ke device yang sama (`.to(device)`).")
print("4. Simpan bobot menggunakan `model.state_dict()` alih-alih seluruh objek model.")
print("=" * 70)
