# =========================================================
# Strategic Intelligence Core (SIC)
# Strategic Transformer – NO REJECTION MODE
# + WPIL (Winning Posts Intelligence Layer) – REMIX MODE
# AI DOMINATOR V17.0 (WPIL READY)
# =========================================================

from typing import Dict, Any, List, Tuple
from sic_memory import get_platform_score

# ---------------------------------------------------------
# Public Entry
# ---------------------------------------------------------
def strategic_intelligence_core(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transforms any raw idea into a dominance-ready execution plan.
    Guaranteed execution. No rejection.
    Adds WPIL Remix Mode when winning posts are provided.
    """

    content = payload.get("content_signal", {}) or {}
    style = payload.get("style_signal", {}) or {}
    context = payload.get("context_signal", {}) or {}
    wpil = payload.get("wpil_signal", {}) or {}

    raw_text = (
        content.get("raw_text")
        or content.get("topic")
        or payload.get("text")
        or ""
    ).strip()

    # --- Base metrics + dominance injection ---
    metrics = _evaluate_metrics(raw_text)
    transformed_text, metrics = _inject_dominance(raw_text, metrics)

    # --- WPIL (Winning Posts) ---
    winning_posts = _normalize_winning_posts(wpil.get("winning_posts"))
    niche = (wpil.get("niche") or context.get("niche") or "").strip()
    voice = (wpil.get("voice_profile") or style.get("style_dna") or "Professional").strip()

    wpil_mode = "off"
    wpil_pack = None
    generation_directives = _default_generation_directives()

    if winning_posts:
        wpil_mode = "remix"
        wpil_pack = _extract_winning_patterns(winning_posts, niche=niche)
        generation_directives = _build_generation_directives_from_wpil(
            wpil_pack=wpil_pack,
            voice=voice,
            niche=niche,
            metrics=metrics
        )

    # --- Platform selection ---
    platforms = _select_platforms(metrics, context)
    if not platforms:
        platforms = ["linkedin", "twitter", "tiktok"]

    platforms.sort(key=lambda p: get_platform_score(p), reverse=True)
    primary = platforms[0]
    secondary = platforms[1:]

    return {
        "execute": True,
        "primary_platform": primary,
        "secondary_platforms": secondary,
        "content_mode": _content_mode_for(primary),

        # Important: keep compatibility
        "style_override": style.get("style_dna", "Professional"),
        "rules": {
            "hook_required": True,
            "cta_type": "curiosity",
            "length": _content_length(metrics),
        },

        # Input transformed (still used by generators)
        "transformed_input": transformed_text,

        # WPIL output (NEW)
        "wpil": {
            "mode": wpil_mode,                 # off | remix
            "niche": niche,
            "has_winning_posts": bool(winning_posts),
            "pack": wpil_pack,                 # compact patterns summary (NO copying)
            "generation_directives": generation_directives
        },

        "decision_reason": "Auto-transformed for dominance (no rejection mode) + WPIL remix ready",
    }

# ---------------------------------------------------------
# WPIL Helpers
# ---------------------------------------------------------
def _normalize_winning_posts(items: Any) -> List[str]:
    """
    Accepts:
    - List[str]
    - str (single block)
    - None
    Returns list[str] with safe trimming.
    """
    if not items:
        return []

    if isinstance(items, str):
        s = items.strip()
        return [s] if s else []

    if isinstance(items, list):
        out = []
        for x in items:
            if isinstance(x, str):
                s = x.strip()
                if s:
                    out.append(s)
        return out

    return []

def _extract_winning_patterns(winning_posts: List[str], niche: str = "") -> Dict[str, Any]:
    """
    Extracts non-copyright patterns (structure & tactics) ONLY.
    Does not copy or reproduce posts. Produces a compact 'pattern pack'.
    """
    sample = winning_posts[:8]  # cap for safety

    hooks = []
    structures = {"numbered": 0, "bullets": 0, "story": 0, "question_open": 0}
    cta_types = {"comment": 0, "save": 0, "share": 0, "dm": 0, "follow": 0}
    tone_hints = {"direct": 0, "curious": 0, "contrarian": 0, "empathetic": 0}

    for p in sample:
        first_line = _first_nonempty_line(p)[:160]
        if first_line:
            hooks.append(_sanitize_hook(first_line))

        s = p.lower()
        if any(tok in s for tok in ["1)", "2)", "3)", "1- ", "2- ", "3- "]):
            structures["numbered"] += 1
        if "•" in p or "- " in p:
            structures["bullets"] += 1
        if any(tok in s for tok in ["كنت", "صار", "حدث", "تعلمت", "في يوم"]):
            structures["story"] += 1
        if "?" in first_line:
            structures["question_open"] += 1

        if any(tok in s for tok in ["اكتب", "علق", "comment"]):
            cta_types["comment"] += 1
        if any(tok in s for tok in ["احفظ", "save"]):
            cta_types["save"] += 1
        if any(tok in s for tok in ["شارك", "share"]):
            cta_types["share"] += 1
        if any(tok in s for tok in ["راسلني", "dm", "رسالة"]):
            cta_types["dm"] += 1
        if any(tok in s for tok in ["تابع", "follow"]):
            cta_types["follow"] += 1

        if any(tok in s for tok in ["ببساطة", "باختصار", "مباشرة"]):
            tone_hints["direct"] += 1
        if any(tok in s for tok in ["ماذا لو", "تخيل", "هل"]):
            tone_hints["curious"] += 1
        if any(tok in s for tok in ["الحقيقة", "خطأ", "لا أحد", "غير المريح"]):
            tone_hints["contrarian"] += 1
        if any(tok in s for tok in ["أفهم", "مررت", "صعب", "طبيعي"]):
            tone_hints["empathetic"] += 1

    top_structure = _argmax(structures)
    top_cta = _argmax(cta_types)
    top_tone = _argmax(tone_hints)

    # compact hook templates (NOT the originals)
    hook_templates = _derive_hook_templates(hooks)

    return {
        "niche": niche,
        "sample_size": len(sample),
        "top_structure": top_structure,
        "top_cta": top_cta,
        "top_tone": top_tone,
        "hook_templates": hook_templates,
        "winning_signals": {
            "structures": structures,
            "cta_types": cta_types,
            "tone_hints": tone_hints,
        }
    }

def _build_generation_directives_from_wpil(
    wpil_pack: Dict[str, Any],
    voice: str,
    niche: str,
    metrics: Dict[str, float]
) -> Dict[str, Any]:
    """
    Outputs strict directives for the generator prompts.
    The generator should follow these, and must create 'novel' content.
    """
    structure = (wpil_pack or {}).get("top_structure", "numbered")
    cta = (wpil_pack or {}).get("top_cta", "comment")
    tone = (wpil_pack or {}).get("top_tone", "curious")
    hook_templates = (wpil_pack or {}).get("hook_templates", [])

    # Choose CTA style based on our own dominance metrics too
    cta_final = "curiosity"
    if cta in ("save", "share"):
        cta_final = cta
    elif metrics.get("share", 0.0) < 0.7:
        cta_final = "comment"

    return {
        "mode": "REMIX_NOVEL",
        "voice_profile": voice,
        "niche": niche,

        "structure_policy": {
            "preferred": structure,         # numbered | bullets | story | question_open
            "must_include": ["hook", "value", "twist", "cta"],
            "format_guardrails": [
                "no copying",
                "no paraphrase-too-close",
                "new examples",
                "new framing",
                "new phrasing",
            ],
        },

        "hook_policy": {
            "use_templates": hook_templates[:3],
            "hook_strength": "max",
            "pattern_interrupt": True
        },

        "value_policy": {
            "deliver_value_fast": True,
            "use_concrete_steps": True,
            "add_personal_micro_story": True
        },

        "tone_policy": {
            "dominant_tone": tone,          # direct | curious | contrarian | empathetic
            "clarity": "high",
            "density": "high",
        },

        "cta_policy": {
            "type": cta_final,              # curiosity | comment | save | share
            "style": "soft_power",
        },

        "novelty_policy": {
            "novelty_score_target": 0.85,
            "ban_phrases": [
                "هذا المنشور",
                "كما في المنشور الأصلي",
                "حسب النص التالي"
            ],
            "must_add": [
                "fresh angle",
                "fresh example",
                "fresh micro-contradiction"
            ]
        }
    }

def _default_generation_directives() -> Dict[str, Any]:
    return {
        "mode": "STANDARD",
        "structure_policy": {"preferred": "numbered"},
        "hook_policy": {"pattern_interrupt": True},
        "cta_policy": {"type": "curiosity"},
        "novelty_policy": {"novelty_score_target": 0.75}
    }

def _first_nonempty_line(text: str) -> str:
    for line in text.splitlines():
        s = line.strip()
        if s:
            return s
    return ""

def _sanitize_hook(hook: str) -> str:
    # remove heavy specifics to avoid closeness; keep only shape
    h = hook.strip()
    # simple neutralization
    h = h.replace("…", "...")
    return h

def _derive_hook_templates(hooks: List[str]) -> List[str]:
    """
    Convert sampled hooks into generic templates (shapes), not copies.
    """
    templates = []
    for h in hooks[:6]:
        l = h.lower()
        if "ماذا لو" in l or "what if" in l:
            templates.append("ماذا لو كان {belief} خطأ تمامًا؟")
        elif "الحقيقة" in l or "truth" in l:
            templates.append("الحقيقة غير المريحة: {claim}")
        elif "?" in h:
            templates.append("سؤال صادم: {question}?")
        elif any(x in l for x in ["5", "7", "10", "أخطاء", "خطوات", "طرق"]):
            templates.append("{n} أشياء تغيّر {domain} بالكامل")
        else:
            templates.append("هذا سيغيّر طريقة فهمك لـ {topic}")
    # unique
    uniq = []
    for t in templates:
        if t not in uniq:
            uniq.append(t)
    return uniq[:5]

def _argmax(d: Dict[str, int]) -> str:
    if not d:
        return ""
    return max(d.items(), key=lambda x: x[1])[0]

# ---------------------------------------------------------
# Dominance Injection
# ---------------------------------------------------------
def _inject_dominance(text: str, metrics: Dict[str, float]) -> Tuple[str, Dict[str, float]]:
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
