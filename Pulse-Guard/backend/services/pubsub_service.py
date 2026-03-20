import asyncio
import logging
from services.reasoning_agent import process_event

logger = logging.getLogger(__name__)

async def publish_event(event_data: dict):
    """
    Mock for Google Cloud Pub/Sub logic to trigger the Reasoning Agent.
    In real usage, this would publish to a Pub/Sub topic.
    For local simulation, we just call the processor asynchronously.
    """
    logger.info(f"Publishing event to Reasoning Agent: {event_data['type']}")
    # Simulate slight network delay
    await asyncio.sleep(0.1)
    await process_event(event_data)
