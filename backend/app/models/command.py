from datetime import datetime
from typing import Optional, Any
from sqlalchemy import String, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class ActuatorCommand(Base):
    __tablename__ = "actuator_commands"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Jenis perintah: misal 'water'
    command_type: Mapped[str] = mapped_column(String(50), nullable=False)

    # Payload fleksibel, misal {"duration_seconds": 10}
    payload: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON, nullable=True)

    # Status: 'pending' (antri), 'sent' (diambil IoT), 'ack' (dikonfirmasi sukses)
    status: Mapped[str] = mapped_column(String(20), default="pending", index=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
