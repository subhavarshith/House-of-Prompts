from fastapi import APIRouter, File, UploadFile, BackgroundTasks
from pydantic import BaseModel
import logging
from services.pubsub_mock import publish_event
import time
import state

router = APIRouter()
logger = logging.getLogger(__name__)

class TelemetryData(BaseModel):
    heart_rate: int
    motion: int

@router.post("/telemetry")
async def receive_telemetry(data: TelemetryData, background_tasks: BackgroundTasks):
    logger.info(f"Received telemetry: HR={data.heart_rate}, Motion={data.motion}")
    
    event_payload = {"type": "telemetry", "data": data.dict(), "timestamp": time.time()}
    state.add_event({"category": "input", "payload": event_payload})
    
    # Trigger Pub/Sub event for Reasoning Agent
    background_tasks.add_task(publish_event, event_payload)
    return {"status": "telemetry received"}

@router.post("/upload-audio")
async def receive_audio(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    # In a real app we would upload to GCS here. For local MVP we save to disk.
    content = await file.read()
    file_path = f"test_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(content)
        
    logger.info(f"Received audio file: {file.filename}")
    event_payload = {"type": "audio", "file_path": file_path, "filename": file.filename, "timestamp": time.time()}
    state.add_event({"category": "input", "payload": event_payload})
    
    if background_tasks:
        background_tasks.add_task(publish_event, event_payload)
    return {"status": "audio received", "filename": file.filename}
