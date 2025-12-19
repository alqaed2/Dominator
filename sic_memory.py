# =========================================================
# SIC Memory — Lightweight Platform Scoring + Feedback
# =========================================================

from __future__ import annotations
from typing import Dict, Any
import os
import json
import time

MEMORY_FILE = os.getenv("SIC_MEMORY_FILE", "sic_memory.json")

# Base scores (static bias). Tweak as you like.
_BASE: Dict[str, float] = {
    "linkedin": 0.90,
    "twitter":  0.82,
    "tiktok":   0.78,
}

def _now() -> int:
    return int(time.time())

def _load() -> Dict[str, Any]:
    try:
        if not os.path.exists(MEMORY_FILE):
            return {"updated_at": _now(), "platforms": {}}
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        # If file is corrupted or unreadable, fail safe.
        return {"updated_at": _now(), "platforms": {}}

def _save(data: Dict[str, Any]) -> None:
    try:
        data["updated_at"] = _now()
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        # Fail silently (Render FS can be ephemeral; do not crash requests)
        pass

def _ensure_platform(data: Dict[str, Any], platform: str) -> Dict[str, int]:
    plats = data.setdefault("platforms", {})
    if platform not in plats:
        plats[platform] = {"success": 0, "failure": 0}
    return plats[platform]

def record_success(platform: str) -> None:
    platform = (platform or "").strip().lower()
    if platform not in _BASE:
        return
    data = _load()
    p = _ensure_platform(data, platform)
    p["success"] += 1
    _save(data)

def record_failure(platform: str) -> None:
    platform = (platform or "").strip().lower()
    if platform not in _BASE:
        return
    data = _load()
    p = _ensure_platform(data, platform)
    p["failure"] += 1
    _save(data)

def get_platform_score(platform: str) -> float:
    """
    Returns a stable score in [0, 1.2] approx.
    Used for sorting platforms — MUST remain deterministic and safe.
    """
    platform = (platform or "").strip().lower()
    base = _BASE.get(platform, 0.50)

    data = _load()
    p = data.get("platforms", {}).get(platform, {"success": 0, "failure": 0})
    s = int(p.get("success", 0))
    f = int(p.get("failure", 0))
    total = s + f

    # Simple reliability bonus/penalty, capped.
    if total == 0:
        adj = 0.0
    else:
        rate = s / total
        # Map 0..1 to -0.05..+0.05
        adj = (rate - 0.5) * 0.10

    score = base + adj
    # Keep within sane bounds:
    if score < 0.10:
        score = 0.10
    if score > 1.20:
        score = 1.20
    return float(score)
