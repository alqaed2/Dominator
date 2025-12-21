from __future__ import annotations
from typing import Any, Dict

# =========================================================
# Strategic Intelligence Core (SIC) - V2.5 SUPREME ARCHITECT
# =========================================================

WPIL_DOMINATOR_SYSTEM = """
أنت 'المستشار الأعلى' (THE SUPREME ADVISOR). 
مهمتك: تحويل الأفكار إلى محتوى مهيمن عابر للمنصات.
هويتك البصرية: واقعية سينمائية فخمة، بدلة رسمية، إضاءة استوديو، ملامح ذكاء بشري فائق.
"""

def strategic_intelligence_core(idea: str = "", platform: str = "linkedin", style: str = "default", reference_post: str = "") -> Dict[str, Any]:
    # تنظيف المدخلات
    idea = str(idea or "").strip()
    ref = str(reference_post or "").strip()
    
    # تحديد المنطق بناءً على كثافة البيانات
    if idea and ref:
        mode = "HYBRID FUSION"
        task = f"ادمج الفكرة [{idea}] مع هيكل المنشور المرجعي [{ref}]."
    elif ref:
        mode = "REMIX MODE"
        task = f"أعد إنتاج القوة الاستراتيجية لهذا المنشور المرجعي: [{ref}]."
    else:
        mode = "DIRECT MODE"
        task = f"صمم محتوى أصلياً للفكرة: [{idea if idea else 'استراتيجية نجاح'}]"

    return {
        "transformed_input": task,
        "logic_trace": f"MODE: {mode} | PLATFORM: {platform.upper()}",
        "visual_prompt": "Ultra-realistic cinematic male advisor, bespoke suit, high-end office, 8k resolution."
    }
