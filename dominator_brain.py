# =========================================================
# Strategic Intelligence Core (SIC)
# Strategic Transformer – Stable Mode (No Confusing Outputs)
# AI DOMINATOR V16.3+ (PATCHED)
# =========================================================

from __future__ import annotations
from typing import Dict, Any, List, Tuple
from sic_memory import get_platform_score

_ALLOWED_PLATFORMS = ("linkedin", "twitter", "tiktok")

def strategic_intelligence_core(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transforms any raw idea into a dominance-ready execution plan.
    Always returns a valid primary platform in: linkedin/twitter/tiktok.
    """

    content = payload.get("content_signal", {}) or {}
    style = payload.get("style_signal", {}) or {}
    context = payload.get("context_signal", {}) or {}

    raw_text = (
        content.get("raw_text")
        or content.get("topic")
        or payload.get("text")
        or ""
    )
    raw_text = (raw_text or "").strip()

    metrics = _evaluate_metrics(raw_text)
    transformed_text, metrics = _inject_dominance(raw_text, metrics)

    platforms = _select_platforms(metrics, context)
    if not platforms:
        platforms = list(_ALLOWED_PLATFORMS)

    # Normalize + filter (safety)
    platforms = [_normalize_platform(p) for p in platforms]
    platforms = [p for p in platforms if p in _ALLOWED_PLATFORMS]
    if not platforms:
        platforms = list(_ALLOWED_PLATFORMS)

    platforms.sort(key=lambda p: get_platform_score(p), reverse=True)

    primary = platforms[0]
    secondary = platforms[1:]

    return {
        "execute": True,
        "primary_platform": primary,
        "secondary_platforms": secondary,
        "content_mode": _content_mode_for(primary),
        "style_override": style.get("style_dna", "Professional"),
        "rules": {
            "hook_required": True,
            "cta_type": "curiosity",
            "length": _content_length(metrics),
        },
        "metrics": metrics,
        "transformed_input": transformed_text,
        "decision_reason": "Auto-transformed for dominance (patched stable routing)",
    }

# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------
def _normalize_platform(p: str) -> str:
    p = (p or "").strip().lower()
    # common aliases
    if p in ("x", "tweet", "tweets"):
        return "twitter"
    if p in ("tt", "tik tok", "tik-tok"):
        return "tiktok"
    return p

def _inject_dominance(text: str, metrics: Dict[str, float]) -> Tuple[str, Dict[str, float]]:
    """
    IMPORTANT: Do not stack 4 prefixes blindly (it makes output noisy).
    We apply at most 2 injections based on the weakest metrics.
    """
    t = (text or "").strip()

    # If empty, still create something safe
    if not t:
        t = "فكرة: كيف نصنع قيمة حقيقية بدل الانشغال الزائف؟"

    candidates = []

    if metrics["curiosity"] < 0.70:
        candidates.append(("curiosity", 0.85, lambda x: f"ماذا لو كان هذا مختلفًا تمامًا عمّا تعتقد؟ {x}"))

    if metrics["hook"] < 0.60:
        candidates.append(("hook", 0.80, lambda x: f"{x} — هذه ليست تنبؤات… هذه إشارات مبكرة."))

    if metrics["shock"] < 0.60:
        candidates.append(("shock", 0.75, lambda x: f"الحقيقة غير المريحة: {x}"))

    if metrics["share"] < 0.60:
        candidates.append(("share", 0.80, lambda x: f"ستفهم بعد لحظات لماذا يهتم الناس فعلًا بهذا: {x}"))

    # Sort by lowest metric first, apply max 2
    candidates.sort(key=lambda item: metrics[item[0]])
    applied = 0
    for key, new_val, fn in candidates:
        if applied >= 2:
            break
        t = fn(t)
        metrics[key] = max(metrics[key], new_val)
        applied += 1

    return t, metrics

def _evaluate_metrics(text: str) -> Dict[str, float]:
    t = (text or "").lower()
    length = len(t)

    curiosity = 0.50 + (0.25 if "?" in t else 0.0)
    shock = 0.40 + (0.35 if any(w in t for w in ["الحقيقة", "لن", "لا أحد", "خطير"]) else 0.0)
    skim = 0.60 + (0.20 if length < 280 else 0.0)
    share = 0.50 + (0.30 if any(w in t for w in ["أنت", "لك", "لماذا"]) else 0.0)
    hook = 0.50 + (0.25 if length < 140 else 0.0)

    return {
        "curiosity": min(curiosity, 1.0),
        "shock": min(shock, 1.0),
        "skim": min(skim, 1.0),
        "share": min(share, 1.0),
        "hook": min(hook, 1.0),
    }

def _select_platforms(metrics: Dict[str, float], context: Dict[str, Any]) -> List[str]:
    available = context.get("platforms_available", list(_ALLOWED_PLATFORMS))
    available = [_normalize_platform(p) for p in available]
    available = [p for p in available if p in _ALLOWED_PLATFORMS]

    selected: List[str] = []

    if "twitter" in available and (metrics["curiosity"] + metrics["skim"]) >= 1.60:
        selected.append("twitter")

    if "linkedin" in available and (metrics["curiosity"] + metrics["share"]) >= 1.50:
        selected.append("linkedin")

    if "tiktok" in available and (metrics["shock"] + metrics["hook"]) >= 1.40:
        selected.append("tiktok")

    return selected

def _content_mode_for(platform: str) -> str:
    return {
        "twitter": "thread",
        "linkedin": "post",
        "tiktok": "video",
    }.get(platform, "post")

def _content_length(metrics: Dict[str, float]) -> str:
    if metrics["skim"] > 0.80:
        return "short"
    if metrics["curiosity"] > 0.85:
        return "medium"
    return "long"
