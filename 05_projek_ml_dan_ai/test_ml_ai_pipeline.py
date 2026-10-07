"""
Integration Test Suite untuk Seluruh Pipeline ML/AI (Modul 05)
Memastikan seluruh komponen NumPy, Pandas, Scikit-learn, PyTorch, dan AI Agent
berjalan tanpa error dan menghasilkan output valid.
"""

import unittest
import sys
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from sklearn.ensemble import RandomForestClassifier
import math

class TestPipelineMLAI(unittest.TestCase):

    def test_numpy_dan_pandas_data_processing(self):
        """Memverifikasi kalkulasi array dan pengisian missing value pandas."""
        arr = np.array([1, 2, 3, 4, 5])
        self.assertEqual(arr.sum(), 15)
        self.assertEqual(arr.mean(), 3.0)

        df = pd.DataFrame({"a": [10.0, np.nan, 30.0]})
        df_imputed = df.fillna(df.mean())
        self.assertEqual(df_imputed["a"].isna().sum(), 0)
        self.assertEqual(df_imputed["a"].iloc[1], 20.0)

    def test_scikit_learn_classifier(self):
        """Memverifikasi training dan inferensi model Machine Learning."""
        X = np.array([[1, 2], [2, 3], [10, 12], [11, 13]])
        y = np.array([0, 0, 1, 1])

        clf = RandomForestClassifier(n_estimators=10, random_state=42)
        clf.fit(X, y)
        pred = clf.predict([[1.5, 2.5], [10.5, 12.5]])
        self.assertEqual(list(pred), [0, 1])

    def test_pytorch_tensor_dan_gradient(self):
        """Memverifikasi Autograd engine PyTorch."""
        w = torch.tensor([2.0], requires_grad=True)
        loss = w ** 3
        loss.backward()
        # d(w^3)/dw = 3 * w^2 = 3 * 4 = 12.0
        self.assertAlmostEqual(w.grad.item(), 12.0, places=4)

    def test_pytorch_neural_network_forward(self):
        """Memverifikasi arsitektur neural network linier."""
        model = nn.Sequential(
            nn.Linear(3, 8),
            nn.ReLU(),
            nn.Linear(8, 2)
        )
        dummy_input = torch.randn(4, 3) # Batch size 4, 3 fitur
        output = model(dummy_input)
        self.assertEqual(output.shape, (4, 2))

    def test_vector_similarity_math(self):
        """Memverifikasi perhitungan Cosine Similarity."""
        def cosine(a, b):
            dot = sum(x * y for x, y in zip(a, b))
            norm_a = math.sqrt(sum(x * x for x in a))
            norm_b = math.sqrt(sum(y * y for y in b))
            return dot / (norm_a * norm_b)

        v1 = [1.0, 0.0]
        v2 = [1.0, 0.0]
        v3 = [0.0, 1.0]

        self.assertAlmostEqual(cosine(v1, v2), 1.0, places=4)
        self.assertAlmostEqual(cosine(v1, v3), 0.0, places=4)

if __name__ == "__main__":
    print("=" * 70)
    print("🧪 Menjalankan Verifikasi Suite ML & AI...")
    print("=" * 70)
    unittest.main(verbosity=2)
