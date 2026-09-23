"""
AI usage limits and emergency kill switch enforcement.
Protects AI endpoints against runaway usage, quota exhaustion, and abuse.
"""
from datetime import datetime
from typing import Dict
from collections import defaultdict
from fastapi import HTTPException, status
from app.core.settings import settings
from app.core.security_logging import log_security_event

class AILimitsManager:
    def __init__(self):
        # Maps (user_id, date_str) -> int request count
        self.daily_counts: Dict[str, int] = defaultdict(int)

    def _get_key(self, user_id: str) -> str:
        today = datetime.utcnow().strftime("%Y-%m-%d")
        return f"{user_id}:{today}"

    def get_user_daily_usage(self, user_id: str) -> int:
        return self.daily_counts[self._get_key(user_id)]

    def check_and_increment(self, user_id: str, ip: str = "unknown"):
        """
        Enforces AI Kill Switch and Daily AI Limits.
        Raises HTTPException(503) if AI is disabled.
        Raises HTTPException(429) if daily limit is reached.
        """
        # 1. Kill Switch Check
        if not settings.ai_enabled:
            log_security_event(
                event_type="KILL_SWITCH_ACTIVE",
                ip=ip,
                user_id=user_id,
                details={"message": "AI execution blocked by emergency kill switch"},
                severity="WARNING"
            )
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="AI services are temporarily disabled by the administrator."
            )

        # 2. Daily Limit Check
        key = self._get_key(user_id)
        current_count = self.daily_counts[key]
        
        if current_count >= settings.ai_daily_limit:
            log_security_event(
                event_type="AI_QUOTA_EXCEEDED",
                ip=ip,
                user_id=user_id,
                details={
                    "current_usage": current_count,
                    "daily_limit": settings.ai_daily_limit
                },
                severity="WARNING"
            )
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Daily AI usage limit of {settings.ai_daily_limit} runs exceeded. Quota resets at 00:00 UTC."
            )

        # Increment usage
        self.daily_counts[key] += 1

ai_limits_manager = AILimitsManager()
