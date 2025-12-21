from __future__ import annotations
from typing import Any, Dict

# =========================================================
# Strategic Intelligence Core (SIC) - V2.4 SUPREME FUSION
# =========================================================

WPIL_DOMINATOR_SYSTEM = """
أنت 'المستشار الأعلى' (THE SUPREME ADVISOR). 
قوتك في 'الذكاء التركيبي': دمج الأفكار مع هياكل المحتوى العالمية.
هويتك البصرية: فخامة سينمائية (Luxury Realism).
"""

def strategic_intelligence_core(idea: str = "", platform: str = "linkedin", style: str = "default", reference_post: str = "") -> Dict[str, Any]:
    """
    الدماغ الاستراتيجي: يعالج المدخلات ويدمج الفكرة مع المنشور المرجعي بذكاء مطلق.
    """
    # تنظيف المدخلات لضمان عدم وجود فراغات وهمية
    primary_subject = str(idea or "").strip()
    ref_content = str(reference_post or "").strip()
    
    # اختيار وضع التشغيل بناءً على المعطيات المتوفرة
    if ref_content and primary_subject:
        transformed_task = f"مهمة دمج: خذ الفكرة [{primary_subject}] وصبها في قالب المنشور المرجعي [{ref_content}]. حافظ على القوة والتأثير."
        logic_mode = "HYBRID FUSION (Full Power)"
    elif ref_content:
        transformed_task = f"مهمة ريمكس: أعد إنتاج القوة الاستراتيجية لهذا المنشور المرجعي: [{ref_content}]."
        logic_mode = "REMIX MODE"
    else:
        # إذا لم يتوفر إلا الفكرة أو كانت محاولة تشغيل بالحد الأدنى
        final_idea = primary_subject if primary_subject else "استراتيجية هيمنة شاملة"
        transformed_task = f"مهمة توليد أصلي: صمم محتوى عالي السلطة للفكرة التالية: [{final_idea}]."
        logic_mode = "DIRECT MODE"

    visual_identity = (
        "Ultra-realistic cinematic 8k, high-status male strategic advisor, "
        "bespoke suit, sharp eyes, minimalist luxury office, cinematic lighting."
    )

    return {
        "execute": True,
        "primary_platform": platform,
        "transformed_input": transformed_task,
        "visual_prompt": visual_identity,
        "logic_trace": f"MODE: {logic_mode} | STATUS: SUCCESS"
    }
