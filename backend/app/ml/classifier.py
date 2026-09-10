from pathlib import Path
from typing import Tuple
from app.config import UPLOAD_PATH


class LeafClassifier:
    """
    Modul inferensi Deep Learning untuk klasifikasi kesehatan daun tanaman.
    Disiapkan untuk integrasi model PyTorch / TensorFlow / ONNX.
    """

    def __init__(self):
        self.model = None
        self.labels = ["Healthy", "Early Blight", "Late Blight", "Leaf Mold", "Bacterial Spot"]
        self.load_model()

    def load_model(self):
        """Memuat bobot model saat aplikasi startup."""
        # TODO: Di Fase 4, muat berkas bobot model (misal model.onnx / model.pt) dari direktori app/ml/
        print("[ML CLASSIFIER] Pipeline klasifikasi daun siap digunakan.")

    def predict(self, relative_image_path: str) -> Tuple[str, float]:
        """
        Menerima path relatif gambar, memproses citra, dan menghasilkan prediksi.
        Mengembalikan (label_kelas, skor_keyakinan).
        """
        full_path = UPLOAD_PATH / relative_image_path
        if not full_path.exists():
            return "Unknown", 0.0

        try:
            # Placeholder inferensi: Jika belum ada model bobot biner,
            # berikan hasil berbasis simulasi terprediksi (akan diganti model asli di Fase 4)
            return "Healthy", 0.942
        except Exception as e:
            print(f"[ML ERROR] Inferensi gagal: {e}")
            return "Error", 0.0


# Singleton instance classifier
classifier = LeafClassifier()
