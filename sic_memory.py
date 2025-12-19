# =========================================================
# sic_memory.py
# Simple SIC Memory + Platform Scoring (File-backed JSON)
# =========================================================

from __future__ import annotations
from typing import Dict, Any, List, Optional
import json
import os
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEMORY_FILE = os.path.join(BASE_DIR, "sic_memory_store.json")

# ثابت: درجات منصات افتراضية (يمكن تعديلها لاحقاً من الذاكرة)
DEFAULT_PLATFORM_SCORES = {
    "linkedin": 0.92,
    "twitter": 0.88,
    "tiktok": 0.85,
}

def _now() -> int:
    return int(time.time())

def _load() -> Dict[str, Any]:
    if not os.path.exists(MEMORY_FILE):
        data = {
            "platform_scores": DEFAULT_PLATFORM_SCORES.copy(),
            "events": []
        }
        _save(data)
        return data

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                raise ValueError("Invalid memory format")
    except Exception:
        data = {
            "platform_scores": DEFAULT_PLATFORM_SCORES.copy(),
            "events": []
        }
        _save(data)
        return data

    # ضمان وجود مفاتيح
    data.setdefault("platform_scores", DEFAULT_PLATFORM_SCORES.copy())
    data.setdefault("events", [])
    return data

def _save(data: Dict[str, Any]) -> None:
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        # على Render قد يكون الـ FS read-only في بعض الحالات — نتجاهل بدون كسر التشغيل
        pass

def get_platform_score(platform: str) -> float:
    mem = _load()
    scores = mem.get("platform_scores", DEFAULT_PLATFORM_SCORES)
    return float(scores.get(platform, 0.5))

def record_success(platform: str, meta: Optional[Dict[str, Any]] = None) -> None:
    mem = _load()
    mem["events"].append({
        "ts": _now(),
        "type": "success",
        "platform": platform,
        "meta": meta or {}
    })
    _save(mem)

def record_failure(platform: str, reason: str = "", meta: Optional[Dict[str, Any]] = None) -> None:
    mem = _load()
    mem["events"].append({
        "ts": _now(),
        "type": "failure",
        "platform": platform,
        "reason": reason,
        "meta": meta or {}
    })
    _save(mem)
