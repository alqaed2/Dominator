# event_bus.py
# =========================================================
# AI DOMINATOR – Event Bus (v13)
# Redis Streams based – Render Compatible
# =========================================================

import os
import json
import time
import uuid
from typing import Dict, Any, Optional

import redis

# ------------------------------------------------------------------
# Redis Connection
# ------------------------------------------------------------------

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

redis_client = redis.Redis.from_url(
    REDIS_URL,
    decode_responses=True,
    socket_timeout=5,
    socket_connect_timeout=5,
)

STREAM_NAME = "dominator_events"


# ------------------------------------------------------------------
# Event Schema (Strict – No Random Fields)
# ------------------------------------------------------------------

def build_event(
    event_type: str,
    payload: Dict[str, Any],
    user_id: Optional[str] = None,
    request_id: Optional[str] = None,
) -> Dict[str, Any]:
    return {
        "event_id": str(uuid.uuid4()),
        "type": event_type,
        "version": "1.0",
        "occurred_at": int(time.time()),
        "request_id": request_id or str(uuid.uuid4()),
        "user_id": user_id or "anonymous",
        "payload": payload,
    }


# ------------------------------------------------------------------
# Publish Event
# ------------------------------------------------------------------

def publish_event(event: Dict[str, Any]) -> str:
    """
    Push event into Redis Stream
    Returns stream message ID
    """
    try:
        message_id = redis_client.xadd(
            STREAM_NAME,
            {"data": json.dumps(event, ensure_ascii=False)},
        )
        return message_id
    except Exception as e:
        raise RuntimeError(f"EVENT_PUBLISH_FAILED: {str(e)}")


# ------------------------------------------------------------------
# Consume Event (Worker usage)
# ------------------------------------------------------------------

def consume_event(
    last_id: str = "0-0",
    block_ms: int = 5000,
) -> Optional[Dict[str, Any]]:
    """
    Blocking read for worker
    """
    try:
        streams = redis_client.xread(
            {STREAM_NAME: last_id},
            block=block_ms,
            count=1,
        )
        if not streams:
            return None

        _, messages = streams[0]
        message_id, fields = messages[0]

        event_data = json.loads(fields["data"])
        event_data["_stream_id"] = message_id

        return event_data
    except Exception as e:
        raise RuntimeError(f"EVENT_CONSUME_FAILED: {str(e)}")


# ------------------------------------------------------------------
# Acknowledge / Delete Event (Optional)
# ------------------------------------------------------------------

def acknowledge_event(stream_id: str) -> None:
    try:
        redis_client.xdel(STREAM_NAME, stream_id)
    except Exception:
        # لا نكسر النظام بسبب ack
        pass
