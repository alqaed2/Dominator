# =========================================================
# Strategic Intelligence Core (SIC)
# AI DOMINATOR – V16.1
# =========================================================

from typing import Dict, List, Any

# 🧠 Memory
from sic_memory import get_platform_score


def strategic_intelligence_core(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Governing decision engine of AI DOMINATOR.
    Returns execution directives only.
    """

    # -----------------------------------------------------
    # 1. Input Validation
    # -----------------------------------------------------
    required_keys = ["content_signal", "style_signal", "context_signal", "system_memory"]
    for key in required_keys:
        if key not in payload:
            return _abort(f"Missing required input: {key}")

    content = payload["content_signal"]
    style = payload["style_signal"]
    context = payload["context_signal"]

    # -----------------------------------------------------
    # 2. Metric Evaluation
    # -----------------------------------------------------
    metrics = _evaluate_metrics(content)

    # -----------------------------------------------------
    # 3. Dominance Law
    # -----------------------------------------------------
    if metrics["curiosity"] < 0.7:
        return _abort("Curiosity Index below dominance threshold")

    if metrics["share"] < 0.6:
        return _abort("Share Trigger below dominance threshold")

    if metrics["hook"] < 0.6:
        return _abort("Hook Strength below dominance threshold")

    # -----------------------------------------------------
    # 4. Platform Selection (Memory-Aware)
    # -----------------------------------------------------
    platforms = _select_platforms(metrics, context)

    if not platforms:
        return _abort("No platform met execution criteria")

    # Sort platforms by historical performance
    platforms.sort(
        key=lambda p: get_platform_score(p),
        reverse=True
    )

    primary = platforms[0]
    secondary = platforms[1:]

    # -----------------------------------------------------
    # 5. Decision Construction
    # -----------------------------------------------------
    decision = {
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
        "decision_reason": f"Platform ranked by performance memory: {platforms}"
    }

    return decision


# =========================================================
# Helpers
# =========================================================

def _evaluate_metrics(content: Dict[str, Any]) -> Dict[str, float]:
    text = (content.get("raw_text") or "").lower()
    length = len(text)

    curiosity = 0.5 + (0.2 if "?" in text else 0.0)
    shock = 0.4 + (0.3 if any(w in text for w in ["never", "nobody", "truth"]) else 0.0)
    skim = 0.6 + (0.2 if length < 300 else 0.0)
    share = 0.5 + (0.3 if any(w in text for w in ["you", "your"]) else 0.0)
    hook = 0.6 if length < 120 else 0.5

    return {
        "curiosity": min(curiosity, 1.0),
        "shock": min(shock, 1.0),
        "skim": min(skim, 1.0),
        "share": min(share, 1.0),
        "hook": min(hook, 1.0)
    }


def _select_platforms(metrics: Dict[str, float], context: Dict[str, Any]) -> List[str]:
    available = context.get("platforms_available", [])
    selected = []

    if "twitter" in available and metrics["curiosity"] + metrics["skim"] >= 1.6:
        selected.append("twitter")

    if "linkedin" in available and metrics["curiosity"] + metrics["share"] >= 1.5:
        selected.append("linkedin")

    if "tiktok" in available and metrics["shock"] + metrics["hook"] >= 1.4:
        selected.append("tiktok")

    return selected


def _content_mode_for(platform: str) -> str:
    return {
        "twitter": "thread",
        "linkedin": "post",
        "tiktok": "video"
    }.get(platform, "post")


def _content_length(metrics: Dict[str, float]) -> str:
    if metrics["skim"] > 0.8:
        return "short"
    if metrics["curiosity"] > 0.8:
        return "medium"
    return "long"


def _abort(reason: str) -> Dict[str, Any]:
    return {
        "execute": False,
        "primary_platform": None,
        "secondary_platforms": [],
        "content_mode": None,
        "style_override": None,
        "rules": {},
        "decision_reason": reason
    }
