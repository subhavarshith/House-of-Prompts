from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import time

class TelemetryData(BaseModel):
    heart_rate: int = Field(..., gt=0, lt=300, description="Heart rate in BPM")
    motion: int = Field(..., ge=0, description="Motion level, 0 means no movement")

class EventPayload(BaseModel):
    type: str
    data: Optional[Dict[str, Any]] = None
    file_path: Optional[str] = None
    filename: Optional[str] = None
    timestamp: float = Field(default_factory=time.time)

class EventLogEntry(BaseModel):
    category: str  # e.g., "input", "reasoning", "action"
    payload: Dict[str, Any]
    timestamp: float = Field(default_factory=time.time)
