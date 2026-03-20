from fastapi import APIRouter, File, UploadFile, BackgroundTasks, HTTPException
from models.telemetry import TelemetryData, EventPayload
import logging
from services.pubsub_service import publish_event
from services.storage_service import upload_to_gcs
import time
import state

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/telemetry")
async def receive_telemetry(data: TelemetryData, background_tasks: BackgroundTasks):
    """
    Ingests IoT telemetry data (Heart Rate and Motion).
    """
    logger.info(f"Received telemetry: HR={data.heart_rate}, Motion={data.motion}")
    
    event_payload = {
        "type": "telemetry", 
        "data": data.dict(), 
        "timestamp": time.time()
    }
    state.add_event({"category": "input", "payload": event_payload})
    
    # Trigger Pub/Sub logic for Reasoning Agent
    background_tasks.add_task(publish_event, event_payload)
    return {"status": "telemetry received", "data": data}

@router.post("/upload-audio")
async def receive_audio(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    """
    Handles audio file uploads for distress call analysis.
    """
    if not file.filename.endswith(('.wav', '.mp3')):
        raise HTTPException(status_code=400, detail="Unsupported file format. Only WAV and MP3 are allowed.")
        
    content = await file.read()
    
    # Use the storage service to 'upload' to GCS
    gcs_uri = await upload_to_gcs(content, file.filename)
    
    logger.info(f"Received audio file: {file.filename} (Stored at: {gcs_uri})")
    
    event_payload = {
        "type": "audio", 
        "file_path": gcs_uri, 
        "filename": file.filename, 
        "timestamp": time.time()
    }
    state.add_event({"category": "input", "payload": event_payload})
    
    if background_tasks:
        background_tasks.add_task(publish_event, event_payload)
        
    return {"status": "audio received", "filename": file.filename, "gcs_uri": gcs_uri}
