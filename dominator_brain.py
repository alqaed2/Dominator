# =========================================================
# Strategic Intelligence Core (SIC)
# NO-REJECTION MODE + WPIL-AWARE
# AI DOMINATOR (STABLE)
# =========================================================

from typing import Dict, Any, List
from sic_memory import get_platform_score


def strategic_intelligence_core(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    يحوّل أي فكرة خام إلى قرار تنفيذ + قواعد إنتاج.
    مبدأ ثابت: لا رفض. دائمًا Execute = True.
    """

    content = payload.get("content_signal", {}) or {}
    style = payload.get("style_signal", {}) or {}
    context = payload.get("context_signal", {}) or {}

    raw_text = (
        content.get("raw_text")
        or content.get("topic")
        or payload.get("text")
        or ""
    ).strip()

    # حتى لو كانت فارغة، لا نكسر النظام
    if not raw_text:
        raw_text = "اكتب فكرة/موضوع وسأحوّلها إلى منشور عالي الأداء."

    metrics = _evaluate_metrics(raw_text)
    transformed_text, metrics = _inject_dominance(raw_text, metrics)

    # WPIL constraints (اختياري)
    wpil_constraints = payload.get("wpil_constraints") or {}
    wpil_mode = payload.get("wpil_mode") or "direct"

    platforms = _select_platforms(metrics, context)
    if not platforms:
        platforms = ["linkedin", "twitter", "tiktok"]

    platforms.sort(key=lambda p: get_platform_score(p), reverse=True)

    primary = platforms[0]
    secondary = platforms[1:]

    rules = {
        "hook_required": True,
        "cta_type": "curiosity",
        "length": _content_length(metrics),
    }

    # دمج WPIL داخل rules بدون أي تقييم/رفض
    if wpil_constraints:
        rules["wpil"] = wpil_constraints
        rules["wpil_mode"] = wpil_mode

    return {
        "execute": True,
        "primary_platform": primary,
        "secondary_platforms": secondary,
        "content_mode": _content_mode_for(primary),
        "style_override": style.get("style_dna", "Professional"),
        "rules": rules,
        "transformed_input": transformed_text,
        "decision_reason": "Auto-transformed for dominance (no rejection mode)",
    }


def _inject_dominance(text: str, metrics: Dict[str, float]):
    t = text

    if metrics["curiosity"] < 0.7:
        t = f"ماذا لو كان هذا مختلفًا تمامًا عمّا تعتقد؟ {t}"
        metrics["curiosity"] = 0.85

    if metrics["hook"] < 0.6:
        t = f"{t} — هذه ليست تنبؤات… هذه إشارات مبكرة."
        metrics["hook"] = 0.8

    if metrics["shock"] < 0.6:
        t = f"الحقيقة غير المريحة: {t}"
        metrics["shock"] = 0.75

    if metrics["share"] < 0.6:
        t = f"أنت على وشك أن ترى لماذا يهتم الناس فعلًا بهذا: {t}"
        metrics["share"] = 0.8

    return t, metrics


def _evaluate_metrics(text: str) -> Dict[str, float]:
    t = (text or "").lower()
    length = len(t)

    curiosity = 0.5 + (0.25 if "?" in t else 0.0)
    shock = 0.4 + (0.35 if any(w in t for w in ["الحقيقة", "لن", "لا أحد", "خطير"]) else 0.0)
    skim = 0.6 + (0.2 if length < 280 else 0.0)
    share = 0.5 + (0.3 if any(w in t for w in ["أنت", "لك", "لماذا"]) else 0.0)
    hook = 0.5 + (0.25 if length < 140 else 0.0)

    return {
        "curiosity": min(curiosity, 1.0),
        "shock": min(shock, 1.0),
        "skim": min(skim, 1.0),
        "share": min(share, 1.0),
        "hook": min(hook, 1.0),
    }


def _select_platforms(metrics: Dict[str, float], context: Dict[str, Any]) -> List[str]:
    available = context.get("platforms_available", ["linkedin", "twitter", "tiktok"])
    selected = []

    if "twitter" in available and (metrics["curiosity"] + metrics["skim"]) >= 1.6:
        selected.append("twitter")

    if "linkedin" in available and (metrics["curiosity"] + metrics["share"]) >= 1.5:
        selected.append("linkedin")

    if "tiktok" in available and (metrics["shock"] + metrics["hook"]) >= 1.4:
        selected.append("tiktok")

    return selected


def _content_mode_for(platform: str) -> str:
    return {
        "twitter": "thread",
        "linkedin": "post",
        "tiktok": "video",
    }.get(platform, "post")


def _content_length(metrics: Dict[str, float]) -> str:
    if metrics["skim"] > 0.8:
        return "short"
    if metrics["curiosity"] > 0.85:
        return "medium"
    return "long"
