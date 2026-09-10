from datetime import datetime
from typing import Optional, Any, List
from pydantic import BaseModel, ConfigDict


class ActuatorCommandCreate(BaseModel):
    command_type: str = "water"
    payload: Optional[dict[str, Any]] = {"duration_seconds": 10}


class ActuatorCommandResponse(BaseModel):
    id: int
    command_type: str
    payload: Optional[dict[str, Any]] = None
    status: str
    created_at: datetime
    sent_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class PendingCommandsResponse(BaseModel):
    commands: List[ActuatorCommandResponse]
