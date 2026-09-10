import uuid
from datetime import datetime
from pathlib import Path
from fastapi import UploadFile, HTTPException, status
from PIL import Image
import io

from app.config import UPLOAD_PATH

# Format gambar yang diizinkan
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 Megabytes


async def save_leaf_image(file: UploadFile) -> str:
    """
    Validasi dan simpan berkas gambar fisik dari perangkat IoT.
    Menghasilkan path relatif: 'YYYY-MM-DD/<uuid>_<filename>'
    """
    # 1. Validasi ekstensi
    file_ext = Path(file.filename or "image.jpg").suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Format berkas tidak didukung: '{file_ext}'. Hanya menerima JPG/PNG.",
        )

    # 2. Baca isi berkas & validasi ukuran
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ukuran berkas melebihi batas maksimum 5MB.",
        )

    # 3. Validasi integritas berkas citra menggunakan Pillow
    try:
        image = Image.open(io.BytesIO(contents))
        image.verify()  # Memastikan berkas tidak korup
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Berkas gambar rusak atau tidak valid.",
        )

    # 4. Tentukan folder tujuan berbasis tanggal upload (YYYY-MM-DD)
    date_folder = datetime.utcnow().strftime("%Y-%m-%d")
    target_dir = UPLOAD_PATH / date_folder
    target_dir.mkdir(parents=True, exist_ok=True)

    # 5. Buat nama berkas unik agar tidak tertimpa
    safe_name = f"{uuid.uuid4().hex[:8]}_{Path(file.filename or 'leaf.jpg').name}"
    target_file = target_dir / safe_name

    # 6. Tulis berkas fisik ke disk
    with open(target_file, "wb") as f:
        f.write(contents)

    # Reset pointer file
    await file.seek(0)

    # Kembalikan path relatif (misal: "2026-09-10/a1b2c3d4_leaf.jpg")
    relative_path = f"{date_folder}/{safe_name}"
    return relative_path
