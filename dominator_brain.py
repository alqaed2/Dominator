# =========================================================
# Strategic Intelligence Core (SIC) - V2.2 HYBRID FUSION
# =========================================================

from __future__ import annotations
from typing import Dict, Any

WPIL_DOMINATOR_SYSTEM = """
أنت 'المستشار الأعلى' (THE SUPREME ADVISOR). 
قوتك تكمن في 'الذكاء التركيبي': دمج الأفكار الخام مع هياكل المحتوى الناجحة عالمياً.
"""

def strategic_intelligence_core(idea: str, platform: str = "linkedin", style: str = "default", reference_post: str = "") -> Dict[str, Any]:
    # منطق الاندماج
    # إذا وجدت فكرة ومنشور مرجعي، ندمجهما. إذا وجد أحدهما، نستخدم المتاح.
    
    primary_subject = (idea or "استراتيجية هيمنة").strip()
    
    if reference_post and idea:
        transformed_task = f"استخدم هيكل وأسلوب المنشور المرجعي التالي: [{reference_post}] لتسليط الضوء على هذه الفكرة: [{primary_subject}]"
        logic_mode = "HYBRID FUSION (Idea + Reference)"
    elif reference_post:
        transformed_task = f"أعد صياغة وهيمنة هذا المنشور: [{reference_post}]"
        logic_mode = "REMIX MODE (Reference Only)"
    else:
        transformed_task = f"صمم محتوى أصلياً للفكرة: [{primary_subject}]"
        logic_mode = "DIRECT MODE (Idea Only)"

    visual_identity = (
        "Ultra-realistic cinematic shot of a high-status strategic advisor, "
        "bespoke dark suit, sharp gaze, sophisticated lighting, obsidian office."
    )

    return {
        "execute": True,
        "primary_platform": platform,
        "transformed_input": transformed_task,
        "visual_prompt": visual_identity,
        "logic_trace": f"MODE: {logic_mode} | PLATFORM: {platform}"
    }
