# =========================================================
# SIC Memory (Lightweight)
# - Platform scoring
# - Success/Failure counters (optional)
# =========================================================

from __future__ import annotations
from typing import Dict, Any, Optional
import os
import json
import time

SIC_STATS_FILE = os.environ.get("SIC_STATS_FILE", "sic_stats.json")

_PLATFORM_SCORE = {
    "linkedin": 0.92,
    "twitter": 0.88,
    "tiktok": 0.84,
}


def get_platform_score(platform: str) -> float:
    if not platform:
        return 0.5
    return _PLATFORM_SCORE.get(platform.lower().strip(), 0.5)


def _load_stats() -> Dict[str, Any]:
    try:
        if os.path.exists(SIC_STATS_FILE):
            with open(SIC_STATS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {
        "total": {"success": 0, "failure": 0},
        "platform": {},
        "last_event": None,
    }


def _save_stats(stats: Dict[str, Any]) -> None:
    try:
        with open(SIC_STATS_FILE, "w", encoding="utf-8") as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
    except Exception:
        # في Render قد تكون الكتابة محدودة حسب البيئة، لا نكسر التشغيل
        pass


def record_success(platform: str, meta: Optional[Dict[str, Any]] = None) -> None:
    stats = _load_stats()
    stats["total"]["success"] = int(stats["total"].get("success", 0)) + 1

    p = (platform or "unknown").lower()
    stats["platform"].setdefault(p, {"success": 0, "failure": 0})
    stats["platform"][p]["success"] = int(stats["platform"][p].get("success", 0)) + 1

    stats["last_event"] = {"ts": int(time.time()), "type": "success", "platform": p, "meta": meta or {}}
    _save_stats(stats)


def record_failure(platform: str, reason: str = "", meta: Optional[Dict[str, Any]] = None) -> None:
    stats = _load_stats()
    stats["total"]["failure"] = int(stats["total"].get("failure", 0)) + 1

    p = (platform or "unknown").lower()
    stats["platform"].setdefault(p, {"success": 0, "failure": 0})
    stats["platform"][p]["failure"] = int(stats["platform"][p].get("failure", 0)) + 1

    stats["last_event"] = {
        "ts": int(time.time()),
        "type": "failure",
        "platform": p,
        "reason": reason,
        "meta": meta or {},
    }
    _save_stats(stats)
