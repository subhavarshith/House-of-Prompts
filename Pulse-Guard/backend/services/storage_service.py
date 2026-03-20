import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

async def upload_to_gcs(file_content: bytes, filename: str, bucket_name: str = "pulse-guard-audio") -> str:
    """
    Simulates uploading a file to Google Cloud Storage.
    In production, this would use the `google-cloud-storage` library.
    """
    # Mocking GCS by writing to a local 'cloud_mock' directory
    mock_storage_path = os.path.join(os.getcwd(), "cloud_mock")
    if not os.path.exists(mock_storage_path):
        os.makedirs(mock_storage_path)
    
    file_path = os.path.join(mock_storage_path, filename)
    with open(file_path, "wb") as f:
        f.write(file_content)
    
    logger.info(f"File {filename} uploaded to GCS bucket {bucket_name}")
    return f"gs://{bucket_name}/{filename}"
