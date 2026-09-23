"""
File upload defense-in-depth utility for Kurukshetra.AI.
Validates extensions, MIME types, file size, and sanitized paths
if file uploads are integrated in future modules.
"""
import os
import re
from pathlib import Path
from fastapi import HTTPException, status

ALLOWED_EXTENSIONS = {".txt", ".pdf", ".json", ".csv", ".png", ".jpg", ".jpeg"}
ALLOWED_MIME_TYPES = {
    "text/plain",
    "application/pdf",
    "application/json",
    "text/csv",
    "image/png",
    "image/jpeg",
}
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB

def sanitize_filename(filename: str) -> str:
    """Strip path traversal characters and non-alphanumeric symbols."""
    clean = os.path.basename(filename)
    clean = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', clean)
    clean = clean.lstrip(".")
    if not clean:
        clean = "uploaded_file"
    return clean

def validate_uploaded_file(filename: str, content: bytes, content_type: str = ""):
    """Validate size, extension, and content type safely."""
    if len(content) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size exceeds 10 MB maximum limit."
        )
    
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"File extension '{ext}' is not permitted."
        )
        
    if content_type and content_type.lower() not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"MIME type '{content_type}' is not allowed."
        )
        
    return sanitize_filename(filename)
