from __future__ import annotations
from typing import Any, Dict, List

# =========================================================
# Strategic Intelligence Core (SIC) - V14.0 CONTEXT GUARDIAN
# =========================================================

WPIL_DOMINATOR_SYSTEM = """
أنت 'المستشار الاستراتيجي الأعلى'. مهمتك: تطوير المنشور المرجعي ليكون أكثر احترافية بـ 10 أضعاف.
القواعد الصارمة:
1. المضمون: يجب أن يكون المحتوى عن (نفس موضوع المنشور المرجعي) تماماً. لا تخرج عن السياق.
2. النبرة: سلطوية، نخبوية، عملية، ومباشرة.
3. التنسيق: استخدم عناوين ضخمة، فواصل واضحة، ونسخاً جاهزة للنشر.
4. التقسيم: [LINKEDIN], [TWITTER], [TIKTOK] وقسم الصور [VISUAL_PROMPT].
"""

def get_elite_character() -> str:
    return "A highly attractive, young (30 years old), charismatic Middle-Eastern elite businessman, sharp jawline, neat beard, premium tailored modern suit, standing in a high-tech penthouse office."

def strategic_intelligence_core(idea: str = "") -> Dict[str, Any]:
    v_force = "Vertical 9:16 portrait, ultra-realistic 8k cinematic, professional mobile framing."
    character = get_elite_character()
    
    scenes = [
        {"time": "0-10s", "prompt": f"Close-up of {character} face, looking intense and confident. {v_force}"},
        {"time": "10-20s", "prompt": f"Medium shot of {character} analyzing a translucent digital e-commerce dashboard. {v_force}"},
        {"time": "20-30s", "prompt": f"Action shot of {character} walking through a clean, automated luxury warehouse. {v_force}"}
    ]
    return {
        "logic_trace": "SIC v14.0 | CONTEXT SECURED | ELITE CHARACTER",
        "video_segments": scenes
    }

def alchemy_fusion_core(gold_posts: List[Dict[str, Any]], niche: str) -> Dict[str, Any]:
    # إجبار الـ AI على الالتزام الحرفي بالموضوع
    source_context = gold_posts[0]['text'] if gold_posts else "التجارة الإلكترونية"
    task = f"""
    الموضوع المرجعي: {source_context}
    الهدف: حول هذا العرض العادي إلى 'مرسوم سيادي' يكتسح السوق. 
    اجعل النص العملي (التنفيذ، الأرباح، اللوجستيات) هو الأساس.
    صمم [VISUAL_PROMPT] يصف لقطة فوتوغرافية لـ {get_elite_character()} وهو يدير هذا النشاط.
    """
    return {
        "synthesis_task": task,
        "logic_trace": "CONTEXTUAL SYNTHESIS v14.0"
    }
