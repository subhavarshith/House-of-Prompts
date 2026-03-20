from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import ingestion
import state

app = FastAPI(title="Pulse-Guard API")

# Configure CORS for local development with frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingestion.router, prefix="/api")

@app.get("/api/health")
def read_root():
    return {"status": "Pulse-Guard Backend is running"}

@app.get("/api/events")
def get_events():
    return {"events": state.get_events()}

import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Serve React static build
app.mount("/assets", StaticFiles(directory="static/assets"), name="assets")

@app.get("/{full_path:path}")
async def serve_react(full_path: str):
    return FileResponse("static/index.html")
