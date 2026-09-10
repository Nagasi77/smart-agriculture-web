"""
Skrip Simulasi Perangkat IoT Fisik.
Mengirim paket data sensor berpasangan tepat dengan 1 citra daun ke FastAPI.
"""
import io
import httpx
from datetime import datetime
from PIL import Image

# Konfigurasi simulasi
SERVER_URL = "http://127.0.0.1:8000/api/iot/readings"
IOT_API_KEY = "ganti-dengan-kunci-rahasia-anda"


def generate_dummy_leaf_image() -> bytes:
    """Membuat citra daun tiruan sederhana dalam memori untuk pengujian."""
    img = Image.new("RGB", (300, 300), color=(34, 139, 34))  # Warna hijau daun
    byte_arr = io.BytesIO()
    img.save(byte_arr, format="JPEG")
    return byte_arr.getvalue()


def send_reading():
    print(f"[IOT SIMULATOR] Mengirim data sensor + citra ke {SERVER_URL}...")

    # Data sensor fisik + stempel waktu RTC alat
    form_data = {
        "device_timestamp": datetime.now().isoformat(),
        "temperature": 27.5,
        "humidity": 78.2,
        "soil_moisture": 65.0,
        "light_intensity": 1250.0,
    }

    headers = {
        "X-API-Key": IOT_API_KEY,
    }

    image_bytes = generate_dummy_leaf_image()
    files = {
        "image": ("test_leaf.jpg", image_bytes, "image/jpeg"),
    }

    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.post(SERVER_URL, data=form_data, files=files, headers=headers)
            print(f"Status Code: {response.status_code}")
            print("Response JSON:")
            print(response.json())
    except Exception as e:
        print(f"Gagal mengirim data: {e}")


if __name__ == "__main__":
    send_reading()
