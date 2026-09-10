from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class SensorReadingResponse(BaseModel):
    id: int
    device_timestamp: datetime
    server_timestamp: datetime
    temperature: float
    humidity: float
    soil_moisture: float
    light_intensity: float
    image_path: str
    image_url: str
    classification_result: Optional[str] = None
    confidence_score: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)


class IngestSuccessResponse(BaseModel):
    status: str = "success"
    message: str
    reading_id: int
    classification: Optional[str] = None
    confidence: Optional[float] = None
