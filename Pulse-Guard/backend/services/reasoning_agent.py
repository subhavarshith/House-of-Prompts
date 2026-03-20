import logging
import json
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

import time
from google import genai
from google.genai import types
import state

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# We will need the GEMINI API KEY in environment variables
api_key = os.environ.get("GEMINI_API_KEY")

try:
    if api_key:
        client = genai.Client(api_key=api_key)
    else:
        logger.warning("GEMINI_API_KEY not found in environment. Using default GCP credentials if available.")
        client = genai.Client()
except Exception as e:
    logger.error(f"Failed to initialize GenAI client: {e}")
    client = None

def dispatch_emergency_services(critical_reason: str, required_service: str, location_hint: str):
    """
    Dispatch emergency services when a critical situation is detected.
    
    Args:
        critical_reason: Brief description of why this is an emergency.
        required_service: e.g. "paramedics", "police", "fire".
        location_hint: Any parsed location or default "Unknown".
    """
    payload = {
        "verified": True,
        "action": "dispatch",
        "reason": critical_reason,
        "service": required_service,
        "location": location_hint,
        "timestamp": time.time()
    }
    logger.info(f"*** EMERGENCY DISPATCH TRIGGERED ***")
    logger.info(f"Payload to EMS: {json.dumps(payload, indent=2)}")
    
    state.add_event({"category": "action", "payload": payload})
    return payload

async def process_event(event_data: dict):
    """
    The reasoning bridge that analyzes events using Gemini 3 Flash.
    """
    if not client:
        logger.error("Gemini client not initialized. Cannot process event.")
        return

    logger.info(f"Reasoning Agent analyzing event: {event_data['type']}")
    
    prompt = ""
    # Hardcoded deterministic logic as requested, combined with Gemini function calling
    if event_data['type'] == 'telemetry':
        hr = event_data['data'].get("heart_rate", 0)
        motion = event_data['data'].get("motion", -1)
        if hr > 120 and motion == 0:
            prompt = f"The patient tracker shows a high heart rate ({hr} bpm) and zero motion. This is a critical medical emergency. Call dispatch_emergency_services."
        else:
            prompt = f"The patient tracker shows Heart Rate {hr} bpm and Motion level {motion}. Is this normal?"
    elif event_data['type'] == 'audio':
        # Simulated logic: if we pass an audio file, interpret it.
        # For simplicity in this demo, we textually describe it to Gemini, or if we had real audio we'd upload it using the GenAI File API.
        filename = event_data.get("filename", "")
        # Since this is local dev without real GCS buckets, we will simulate the audio content analysis if the filename has 'distress' or 'thump'.
        if "distress" in filename.lower() or "thump" in filename.lower():
             prompt = f"An audio file '{filename}' was uploaded and it contains sounds of vocal distress and thumps. This is a critical situation. Call dispatch_emergency_services."
        else:
             prompt = f"An audio file '{filename}' was uploaded. Does it sound normal?"

    logger.info(f"Sending prompt to Gemini: {prompt}")

    tool = types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="dispatch_emergency_services",
                description="Dispatch emergency services when a critical situation is detected.",
                parameters={
                    "type": "OBJECT",
                    "properties": {
                        "critical_reason": {"type": "STRING"},
                        "required_service": {"type": "STRING"},
                        "location_hint": {"type": "STRING"}
                    },
                    "required": ["critical_reason", "required_service", "location_hint"]
                }
            )
        ]
    )

    try:
        response = await client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[tool]
            )
        )

        # Check for function call
        if response.function_calls:
            for call in response.function_calls:
                if call.name == "dispatch_emergency_services":
                    # Record the reasoning preceding the call if any
                    if response.text:
                        state.add_event({"category": "reasoning", "payload": {"text": response.text, "timestamp": time.time()}})
                        
                    args = call.args
                    dispatch_emergency_services(
                        critical_reason=args.get("critical_reason"),
                        required_service=args.get("required_service"),
                        location_hint=args.get("location_hint", "Unknown")
                    )
        else:
            logger.info(f"Gemini analysis complete. No emergency detected. Output: {response.text}")
            state.add_event({"category": "reasoning", "payload": {"text": response.text, "timestamp": time.time()}})
    except Exception as e:
        logger.error(f"Error during Gemini processing: {e}")
