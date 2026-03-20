import pytest
from fastapi.testclient import TestClient
from main import app
import state

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "Pulse-Guard Backend is running"

def test_telemetry_ingestion():
    # Clear state for testing
    state.events_log.clear()
    
    payload = {"heart_rate": 80, "motion": 1}
    response = client.post("/api/telemetry", json=payload)
    
    assert response.status_code == 200
    assert response.json()["status"] == "telemetry received"
    
    # Verify it entered the event log
    events = state.get_events()
    assert len(events) == 1
    assert events[0]["category"] == "input"
    assert events[0]["payload"]["data"]["heart_rate"] == 80

def test_invalid_telemetry():
    payload = {"heart_rate": -50, "motion": 1} # Invalid heart rate
    response = client.post("/api/telemetry", json=payload)
    assert response.status_code == 422 # Pydantic validation error

def test_audio_upload_mock():
    # Simulate a file upload
    file_content = b"fake audio data"
    files = {"file": ("test.wav", file_content, "audio/wav")}
    response = client.post("/api/upload-audio", files=files)
    
    assert response.status_code == 200
    assert "gcs_uri" in response.json()
    assert response.json()["filename"] == "test.wav"
