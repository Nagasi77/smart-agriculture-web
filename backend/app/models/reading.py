from datetime import datetime
from typing import Optional
from sqlalchemy import String, Float, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Waktu asli dari RTC perangkat fisik (KUNCI UTAMA PENGURUTAN GROUND TRUTH)
    device_timestamp: Mapped[datetime] = mapped_column(DateTime, index=True, nullable=False)

    # Waktu saat paket diterima oleh server
    server_timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Metrik Lingkungan Fisik
    temperature: Mapped[float] = mapped_column(Float, nullable=False)        # Derajat Celcius
    humidity: Mapped[float] = mapped_column(Float, nullable=False)           # % RH (Kelembapan udara)
    soil_moisture: Mapped[float] = mapped_column(Float, nullable=False)      # % atau ADC kelembapan tanah
    light_intensity: Mapped[float] = mapped_column(Float, nullable=False)    # Lux atau ADC intensitas cahaya

    # Tautan Berkas Gambar Fisik (relatif terhadap direktori uploads)
    image_path: Mapped[str] = mapped_column(String(255), nullable=False)

    # Hasil Inferensi Deep Learning
    classification_result: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    confidence_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    __table_args__ = (
        Index("idx_readings_device_ts_desc", device_timestamp.desc()),
    )
