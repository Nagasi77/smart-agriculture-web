from datetime import datetime
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.middleware.auth import verify_iot_api_key
from app.models.reading import SensorReading
from app.models.command import ActuatorCommand
from app.services.storage import save_leaf_image
from app.ml.classifier import classifier
from app.schemas.reading import IngestSuccessResponse
from app.schemas.command import PendingCommandsResponse, ActuatorCommandResponse

router = APIRouter(dependencies=[Depends(verify_iot_api_key)])


@router.post(
    "/readings",
    response_model=IngestSuccessResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Ingest Data Pasangan Sensor & Foto Daun dari IoT",
)
async def ingest_sensor_and_image(
    device_timestamp: datetime = Form(
        ...,
        description="Waktu RTC asli dari perangkat keras (ISO 8601, contoh: 2026-09-10T14:30:00)",
    ),
    temperature: float = Form(..., description="Suhu lingkungan dalam derajat Celsius"),
    humidity: float = Form(..., description="Kelembapan udara (% RH)"),
    soil_moisture: float = Form(..., description="Kelembapan tanah (% atau ADC)"),
    light_intensity: float = Form(..., description="Intensitas cahaya (lux atau ADC)"),
    image: UploadFile = File(..., description="Foto daun tanaman fisik (JPG/PNG maks 5MB)"),
    db: AsyncSession = Depends(get_db),
):
    """
    Endpoint utama penampung data ground truth:
    1. Memvalidasi kunci statis X-API-Key perangkat.
    2. Menyimpan berkas citra secara fisik ke folder lokal terstruktur.
    3. Menjalankan inferensi klasifikasi model secara otomatis.
    4. Menyimpan seluruh pasangan data ke PostgreSQL.
    """
    # 1. Simpan berkas gambar fisik
    image_rel_path = await save_leaf_image(image)

    # 2. Jalankan inferensi klasifikasi daun
    label, confidence = classifier.predict(image_rel_path)

    # 3. Simpan ke database dengan device_timestamp asli dari RTC
    reading = SensorReading(
        device_timestamp=device_timestamp,
        server_timestamp=datetime.utcnow(),
        temperature=temperature,
        humidity=humidity,
        soil_moisture=soil_moisture,
        light_intensity=light_intensity,
        image_path=image_rel_path,
        classification_result=label,
        confidence_score=confidence,
    )

    db.add(reading)
    await db.commit()
    await db.refresh(reading)

    return IngestSuccessResponse(
        status="success",
        message="Data sensor dan berkas daun berhasil diarsipkan.",
        reading_id=reading.id,
        classification=label,
        confidence=confidence,
    )


@router.get(
    "/commands/pending",
    response_model=PendingCommandsResponse,
    summary="Polling Perintah Aktuator yang Menunggu Dieksekusi",
)
async def get_pending_commands(
    db: AsyncSession = Depends(get_db),
):
    """
    Dipanggil secara berkala oleh alat fisik untuk mengecek apakah ada
    perintah kendali (misal: penyiraman) dari operator dasbor.
    """
    query = (
        select(ActuatorCommand)
        .where(ActuatorCommand.status == "pending")
        .order_by(ActuatorCommand.created_at.asc())
    )
    result = await db.execute(query)
    commands = result.scalars().all()

    return PendingCommandsResponse(
        commands=[ActuatorCommandResponse.model_validate(cmd) for cmd in commands]
    )


@router.post(
    "/commands/{command_id}/ack",
    summary="Konfirmasi Eksekusi Perintah oleh Alat Fisik",
)
async def acknowledge_command(
    command_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Dipanggil alat fisik setelah menerima/menjalankan perintah penyiraman.
    Mengubah status perintah dari 'pending' menjadi 'ack'.
    """
    query = select(ActuatorCommand).where(ActuatorCommand.id == command_id)
    result = await db.execute(query)
    cmd = result.scalar_one_or_none()

    if not cmd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Perintah ID {command_id} tidak ditemukan.",
        )

    cmd.status = "ack"
    cmd.sent_at = datetime.utcnow()
    await db.commit()

    return {
        "status": "success",
        "message": f"Perintah ID {command_id} berhasil dikonfirmasi (ack).",
        "ack_time": cmd.sent_at,
    }
