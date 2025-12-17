# =========================================================
# Strategic Intelligence Core (SIC) — Strategic Transformer
# AI DOMINATOR – V16.2
# =========================================================

from typing import Dict, Any, List
from sic_memory import get_platform_score

# ---------------------------------------------------------
# Public Entry
# ---------------------------------------------------------
def strategic_intelligence_core(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transforms any raw idea into a dominance-ready execution plan.
    No rejection. Only transformation.
    """

    # 1) Extract
    content = payload.get("content_signal", {})
    style = payload.get("style_signal", {})
    context = payload.get("context_signal", {})

    raw_text = (content.get("raw_text") or content.get("topic") or "").strip()

    # 2) Evaluate (initial)
    metrics = _evaluate_metrics(raw_text)

    # 3) Inject Dominance (NO REJECTION)
    transformed_text, metrics = _inject_dominance(raw_text, metrics)

    # 4) Platform Selection (memory-aware)
    platforms = _select_platforms(metrics, context)
    if not platforms:
        platforms = ["linkedin", "twitter", "tiktok"]  # fallback safety

    platforms.sort(key=lambda p: get_platform_score(p), reverse=True)
    primary = platforms[0]
    secondary = platforms[1:]

    # 5) Decision
    return {
        "execute": True,
        "primary_platform": primary,
        "secondary_platforms": secondary,
        "content_mode": _content_mode_for(primary),
        "style_override": style.get("style_dna", "Professional"),
        "rules": {
            "hook_required": True,
            "cta_type": "curiosity",
            "length": _content_length(metrics)
        },
        "transformed_input": transformed_text,
        "decision_reason": f"Transformed for dominance; platform ranked by memory: {platforms}"
    }

# ---------------------------------------------------------
# Dominance Injection
# ---------------------------------------------------------
def _inject_dominance(text: str, metrics: Dict[str, float]):
    t = text

    # Curiosity
    if metrics["curiosity"] < 0.7:
        t = f"ماذا لو كان هذا مختلفًا تمامًا عمّا تعتقد؟ {t}"
        metrics["curiosity"] = 0.85

    # Hook
    if metrics["hook"] < 0.6:
        t = f"{t} — هذه ليست تنبؤات… هذه إشارات مبكرة."
        metrics["hook"] = 0.8

    # Shock
    if metrics["shock"] < 0.6:
        t = f"الحقيقة غير المريحة: {t}"
        metrics["shock"] = 0.75

    # Share
    if metrics["share"] < 0.6:
        t = f"أنت على وشك أن ترى لماذا يهتم الناس فعلًا بهذا: {t}"
        metrics["share"] = 0.8

    return t, metrics

# ---------------------------------------------------------
# Metrics
# ---------------------------------------------------------
def _evaluate_metrics(text: str) -> Dict[str, float]:
    t = text.lower()
    length = len(t)

    curiosity = 0.5 + (0.25 if "?" in t else 0.0)
    shock = 0.4 + (0.35 if any(w in t for w in ["الحقيقة", "لن", "لا أحد", "خطير"]) else 0.0)
    skim = 0.6 + (0.2 if length < 280 else 0.0)
    share = 0.5 + (0.3 if any(w in t
