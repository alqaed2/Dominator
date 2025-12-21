from __future__ import annotations
from typing import Any, Dict

# =========================================================
# Strategic Intelligence Core (SIC) - V2.6 SUPREME STABILITY
# =========================================================

WPIL_DOMINATOR_SYSTEM = """
أنت 'المستشار الأعلى' (THE SUPREME ADVISOR). 
مهمتك: دمج الأفكار مع هياكل المحتوى العالمية لتحقيق الهيمنة.
الهوية: واقعية سينمائية فخمة.
"""

def strategic_intelligence_core(idea: str = "", platform: str = "linkedin", style: str = "default", reference_post: str = "") -> Dict[str, Any]:
    """
    الدماغ الاستراتيجي: يعالج المدخلات مهما كانت مشوهة أو ناقصة.
    """
    idea_clean = str(idea or "").strip()
    ref_clean = str(reference_post or "").strip()
    
    if idea_clean and ref_clean:
        task = f"دمج استراتيجي: صب الفكرة [{idea_clean}] في هيكل [{ref_clean}]"
        mode = "HYBRID FUSION"
    elif ref_clean:
        task = f"ريمكس استراتيجي للمنشور: [{ref_clean}]"
        mode = "REMIX MODE"
    else:
        task = f"توليد أصلي للفكرة: [{idea_clean if idea_clean else 'الهيمنة التقنية'}]"
        mode = "DIRECT MODE"

    return {
        "transformed_input": task,
        "logic_trace": f"MODE: {mode} | PLATFORM: {platform.upper()}",
        "visual_prompt": "Ultra-realistic cinematic male advisor, bespoke suit, high-end obsidian office, 8k."
    }
