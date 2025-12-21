from __future__ import annotations
from typing import Any, Dict

# =========================================================
# Strategic Intelligence Core (SIC) - V2.7 COMPATIBILITY
# =========================================================

WPIL_DOMINATOR_SYSTEM = """
أنت 'المستشار الأعلى' (THE SUPREME ADVISOR). 
هويتك البصرية: واقعية سينمائية فخمة.
"""

def strategic_intelligence_core(idea: str = "", platform: str = "linkedin", style: str = "default", reference_post: str = "") -> Dict[str, Any]:
    # تنظيف المدخلات لضمان عدم وجود فراغات
    idea = str(idea or "").strip()
    ref = str(reference_post or "").strip()
    
    # منطق الاندماج بناءً على المسميات القادمة من index.html
    if idea and ref:
        task = f"دمج: خذ الفكرة [{idea}] وطبق عليها أسلوب المنشور المرجعي [{ref}]"
        mode = "HYBRID FUSION"
    elif ref:
        task = f"ريمكس: أعد إنتاج قوة المنشور التالي استراتيجياً: [{ref}]"
        mode = "REMIX MODE"
    else:
        task = f"توليد: صمم محتوى مهيمن للفكرة: [{idea if idea else 'استراتيجية هيمنة'}]"
        mode = "DIRECT MODE"

    return {
        "transformed_input": task,
        "logic_trace": f"MODE: {mode} | PLATFORM: {platform.upper()}",
        "visual_prompt": "Ultra-realistic cinematic male advisor, bespoke suit, high-end obsidian office."
    }
