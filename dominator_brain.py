from __future__ import annotations
from typing import Any, Dict # هذا السطر هو الذي كان مفقوداً وسبب الانهيار

# =========================================================
# Strategic Intelligence Core (SIC) - V2.3 HYBRID FUSION
# =========================================================

WPIL_DOMINATOR_SYSTEM = """
أنت 'المستشار الأعلى' (THE SUPREME ADVISOR). 
قوتك تكمن في 'الذكاء التركيبي': دمج الأفكار الخام مع هياكل المحتوى الناجحة عالمياً.
هويتك البصرية: واقعية سينمائية فخمة (Luxury Realism).
"""

def strategic_intelligence_core(idea: str = "", platform: str = "linkedin", style: str = "default", reference_post: str = "") -> Dict[str, Any]:
    """
    الدماغ الاستراتيجي: يعالج المدخلات ويدمج الفكرة مع المنشور المرجعي.
    """
    primary_subject = (idea or "استراتيجية هيمنة حديثة").strip()
    ref_content = (reference_post or "").strip()
    
    # منطق الاندماج الفائق
    if ref_content and idea:
        transformed_task = f"ادمج الفكرة التالية: [{primary_subject}] مع أسلوب وهيكل المنشور المرجعي هذا: [{ref_content}]"
        logic_mode = "HYBRID FUSION"
    elif ref_content:
        transformed_task = f"أعد إنتاج القوة التأثيرية لهذا المنشور المرجعي: [{ref_content}]"
        logic_mode = "REMIX MODE"
    else:
        transformed_task = f"صمم محتوى أصلياً للفكرة: [{primary_subject}]"
        logic_mode = "DIRECT MODE"

    # برومبت بصري فخم جداً (المستشار الأعلى)
    visual_identity = (
        "Ultra-realistic cinematic 8k shot of a high-status male strategic advisor, "
        "bespoke charcoal suit, sharp facial features, confident gaze, "
        "minimalist luxury obsidian office background, soft cinematic studio lighting."
    )

    return {
        "execute": True,
        "primary_platform": platform,
        "transformed_input": transformed_task,
        "visual_prompt": visual_identity,
        "logic_trace": f"MODE: {logic_mode} | PLATFORM: {platform}"
    }
