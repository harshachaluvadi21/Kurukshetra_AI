"""
Security logging utility for Kurukshetra.AI.
Ensures sensitive credentials, passwords, tokens, and API keys are NEVER logged.
"""
import logging
import json
import re
from datetime import datetime
from typing import Any, Dict, Optional

# Configure structured security logger
logger = logging.getLogger("kurukshetra.security")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "event": %(message)s}'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

# Sensitive patterns that must never appear in log payloads
REDACTED_PATTERNS = [
    (re.compile(r'(password|passwd|pwd|secret|key|token|access_token|authorization)[\'"]?\s*[:=]\s*[\'"]?([^\s,\'"\}]+)', re.IGNORECASE), r'\1: "[REDACTED]"'),
    (re.compile(r'Bearer\s+[A-Za-z0-9\-\._~\+\/]+=*', re.IGNORECASE), 'Bearer [REDACTED]'),
    (re.compile(r'AIza[0-9A-Za-z-_]{35}'), '[REDACTED_GOOGLE_KEY]'),
    (re.compile(r'gsk_[A-Za-z0-9]{40,}'), '[REDACTED_GROQ_KEY]'),
    (re.compile(r'tvly-[A-Za-z0-9_-]+'), '[REDACTED_TAVILY_KEY]'),
]

def sanitize_for_log(data: Any) -> Any:
    """Recursively scrub sensitive keys and regex patterns."""
    if isinstance(data, dict):
        scrubbed = {}
        for k, v in data.items():
            k_lower = str(k).lower()
            if any(s in k_lower for s in ("password", "secret", "token", "key", "authorization", "credential")):
                scrubbed[k] = "[REDACTED]"
            else:
                scrubbed[k] = sanitize_for_log(v)
        return scrubbed
    elif isinstance(data, list):
        return [sanitize_for_log(item) for item in data]
    elif isinstance(data, str):
        result = data
        for pattern, replacement in REDACTED_PATTERNS:
            result = pattern.sub(replacement, result)
        return result
    return data

def log_security_event(
    event_type: str,
    ip: Optional[str] = None,
    user_id: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    severity: str = "INFO"
):
    """
    Log a structured security event safely.
    Event types:
      - AUTH_LOGIN_SUCCESS
      - AUTH_LOGIN_FAILED
      - AUTH_REGISTER_SUCCESS
      - AUTHZ_VIOLATION (IDOR attempts)
      - RATE_LIMIT_EXCEEDED
      - AI_QUOTA_EXCEEDED
      - KILL_SWITCH_TRIGGERED
      - SUSPICIOUS_INPUT_BLOCKED
      - WS_UNAUTHORIZED_CONNECT
    """
    safe_details = sanitize_for_log(details or {})
    event_payload = {
        "event_type": event_type,
        "ip": ip or "unknown",
        "user_id": str(user_id) if user_id else "anonymous",
        "details": safe_details,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    msg = json.dumps(event_payload)
    if severity == "WARNING":
        logger.warning(msg)
    elif severity == "ERROR":
        logger.error(msg)
    else:
        logger.info(msg)
