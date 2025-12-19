# =========================================================
# Strategic Intelligence Core (SIC)
# Strategic Transformer – Stable + WPIL-aware
# AI DOMINATOR (WPIL + SIC)
# =========================================================

from typing import Dict, Any, List
from sic_memory import get_platform_score

# WPIL Runtime (اختياري)
try:
    from wpil_runtime import invoke_wpil  # type: ignore
except Exception:
    invoke_wpil = None  # fallback


def _safe_invoke_wpil(content_signal: Dict[str, Any]) -> Dict[str, Any]:
    """
    WPIL MUST NOT generate content. It returns enforced constraints only.
    """
    if invoke_wpil is None:
        return {
            "mode": content_signal.get("mode", "DIRECT"),
            "constraints": {
                "hook": {"type": "bold_claim", "max_words": 12},
                "structure": {"line_density": "one_idea_per_line"},
                "cta": {"type": "curiosity", "position": "end"}
            },
            "pattern_count": 0,
            "source": "fallback"
        }
    try:
        return invoke_wpil(content_signal)  # returns Dict
    except Exception:
        return {
            "mode": content_signal.get("mode", "DIRECT"),
            "constraints": {
                "hook": {"type": "bold_claim", "max_words": 12},
                "structure": {"line_density": "one_idea_per_line"},
                "cta": {"type": "curiosity", "position": "end"}
            },
            "pattern_count": 0,
            "source": "error_fallback"
        }


def strategic_intelligence_core(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transforms any raw idea into a dominance-ready execution plan.
    Includes WPIL constraints layer (Winning Pattern Intelligence Layer).
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

    winning_post = (content.get("winning_post") or payload.get("winning_post") or "").strip()
    remix_mode = bool(payload.get("remix")) or bool(winning_post)

    # signals for WPIL
    platform_hint = (content.get("platform") or context.get("platform") or payload.get("platform") or "linkedin").lower()
    niche = (content.get("niche") or context.get("niche") or payload.get("niche") or "general").lower()
    intent = (content.get("intent") or context.get("intent") or payload.get("intent") or "educational").lower()

    if remix_mode:
        mode = "WINNING_POSTS_REMIX"
        wpil_input = {
            "mode": mode,
            "platform": platform_hint,
            "niche": niche,
            "intent": intent,
            "has_winning_post": True
        }
        wpil = _safe_invoke_wpil(wpil_input)

        # SIC لا يكتب المحتوى النهائي هنا — فقط يبني "مدخل" مُهيكل للموديل
        remix_seed = _build_remix_seed(
            winning_post=winning_post or raw_text,
            niche=niche,
            platform=platform_hint,
            style_dna=style.get("style_dna", "Professional"),
            constraints=wpil.get("constraints", {})
        )

        platforms = _select_platforms({"curiosity": 0.9, "skim": 0.8, "share": 0.8, "shock": 0.7, "hook": 0.8}, context)
        if not platforms:
            platforms = [platform_hint, "linkedin", "twitter", "tiktok"]

        platforms = _unique(platforms)
        platforms.sort(key=lambda p: get_platform_score(p), reverse=True)

        return {
            "execute": True,
            "mode": mode,
            "primary_platform": platforms[0],
            "secondary_platforms": platforms[1:],
            "content_mode": _content_mode_for(platforms[0]),
            "style_override": style.get("style_dna", "Professional"),
            "rules": _rules_from_constraints(wpil.get("constraints", {})),
            "transformed_input": remix_seed,
            "wpil_trace": {
                "mode": mode,
                "input": wpil_input,
                "constraints": wpil.get("constraints", {}),
                "pattern_count": wpil.get("pattern_count", 0),
                "source": wpil.get("source", "wpil_runtime")
            },
            "decision_reason": "WPIL Remix Mode (Winning Posts)"
        }

    # DIRECT MODE
    metrics = _evaluate_metrics(raw_text)
    transformed_text, metrics = _inject_dominance(raw_text, metrics)

    mode = "DIRECT"
    wpil_input = {
        "mode": mode,
        "platform": platform_hint,
        "niche": niche,
        "intent": intent,
        "has_winning_post": False
    }
    wpil = _safe_invoke_wpil(wpil_input)

    platforms = _select_platforms(metrics, context)
    if not platforms:
        platforms = [platform_hint, "linkedin", "twitter", "tiktok"]

    platforms = _unique(platforms)
    platforms.sort(key=lambda p: get_platform_score(p), reverse=True)

    return {
        "execute": True,
        "mode": mode,
        "primary_platform": platforms[0],
        "secondary_platforms": platforms[1:],
        "content_mode": _content_mode_for(platforms[0]),
        "style_override": style.get("style_dna", "Professional"),
        "rules": _merge_rules(
            base={
                "hook_required": True,
                "cta_type": "curiosity",
                "length": _content_length(metrics),
            },
            wpil_constraints=wpil.get("constraints", {})
        ),
        "transformed_input": transformed_text,
        "wpil_trace": {
            "mode": mode,
            "input": wpil_input,
            "constraints": wpil.get("constraints", {}),
            "pattern_count": wpil.get("pattern_count", 0),
            "source": wpil.get("source", "wpil_runtime")
        },
        "decision_reason": "Auto-transformed with WPIL constraints"
    }


# ----------------------------
# Helpers
# ----------------------------

def _unique(items: List[str]) -> List[str]:
    seen = set()
    out = []
    for x in items:
        if x not in seen:
            out.append(x)
            seen.add(x)
    return out


def _rules_from_constraints(constraints: Dict[str, Any]) -> Dict[str, Any]:
    hook = constraints.get("hook", {})
    cta = constraints.get("cta", {})
    return {
        "hook_required": True,
        "hook_type": hook.get("type", "bold_claim"),
        "hook_max_words": hook.get("max_words", 12),
        "cta_type": cta.get("type", "curiosity"),
        "cta_position": cta.get("position", "end"),
        "structure": constraints.get("structure", {})
    }


def _merge_rules(base: Dict[str, Any], wpil_constraints: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(base)
    out.update(_rules_from_constraints(wpil_constraints))
    return out


def _build_remix_seed(winning_post: str, niche: str, platform: str, style_dna: str, constraints: Dict[str, Any]) -> str:
    # Seed = تعليمات + المادة المصدر (بدون نسخ حرفي)
    hook = constraints.get("hook", {})
    cta = constraints.get("cta", {})
    structure = constraints.get("structure", {})

    return f"""
[WPIL WINNING POST REMIX SEED]
- niche: {niche}
- platform: {platform}
- style_dna: {style_dna}
- constraints:
  - hook.type: {hook.get("type","bold_claim")}
  - hook.max_words: {hook.get("max_words",12)}
  - structure: {structure}
  - cta.type: {cta.get("type","curiosity")}
  - cta.position: {cta.get("position","end")}

[IMPORTANT]
- ممنوع النسخ الحرفي. أعد بناء الفكرة والهيكل ليبدو جديدًا 100%.
- حافظ على "القوة البنيوية" (Hook → Value → Proof → CTA).
- اجعل النص عربيًا طبيعيًا، بلا مبالغة مفتعلة.

[WINNING_POST_INPUT]
{winning_post}
""".strip()


# ---------------------------------------------------------
# Dominance Injection (DIRECT)
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# Metrics Evaluation
# ---------------------------------------------------------

def _evaluate_metrics(text: str) -> Dict[str, float]:
    t = text.lower()
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


# ---------------------------------------------------------
# Platform Logic
# ---------------------------------------------------------

def _select_platforms(metrics: Dict[str, float], context: Dict[str, Any]) -> List[str]:
    available = context.get("platforms_available", ["linkedin", "twitter", "tiktok"])
    selected: List[str] = []

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
