from __future__ import annotations
from typing import Any, Dict, List

# =========================================================
# Strategic Intelligence Core (SIC) - V5.0 ALCHEMY EDITION
# =========================================================

WPIL_DOMINATOR_SYSTEM = """
أنت 'الخيميائي الاستراتيجي الأعلى' (THE SUPREME ALCHEMIST). 
مهمتك: استقبال مصفوفة من المنشورات الذهبية الناجحة عالمياً، تشريح حمضها النووي (DNA)، وتخليق منشور واحد خارق يتجاوزها جميعاً في القوة والتأثير.
"""

def alchemy_fusion_core(gold_posts: List[Dict[str, Any]], niche: str) -> Dict[str, Any]:
    """
    مفاعل الاندماج: يحول مجموعة منشورات ناجحة إلى 'منشور خارق'.
    """
    # استخراج النصوص الذهبية للتحليل
    dna_samples = [post.get('text', '') for post in gold_posts]
    
    # بناء أمر التخليق (Synthesis Prompt)
    fusion_task = f"""
    المجال المستهدف: {niche}
    العينات الذهبية (DNA Samples):
    {dna_samples}
    
    المطلوب:
    1. استخلص 'الخطاف' الأقوى من العينات.
    2. استخلص 'الهيكل التنظيمي' الأكثر وضوحاً.
    3. ادمج 'الدليل الاجتماعي' والقيمة المضافة.
    4. أنتج 'منشوراً خارقاً' واحداً يجمع هذه القوى.
    """
    
    return {
        "synthesis_task": fusion_task,
        "sources": gold_posts, # للرجوع إليها في الواجهة
        "dominance_score": 98, # تقييم افتراضي للقوة
        "logic_trace": f"SYNTHESIS MODE | FUSED {len(gold_posts)} GOLD SAMPLES | NICHE: {niche}"
    }

def strategic_intelligence_core(idea: str = "", platform: str = "linkedin", style: str = "default", reference_post: str = "") -> Dict[str, Any]:
    # ... (نفس المنطق السابق لضمان استقرار المهام العادية) ...
    v_force = "Vertical 9:16 portrait, high-end studio, elite male advisor."
    return {
        "transformed_input": f"توليد قيادي لـ [{idea or reference_post}]",
        "logic_trace": "DIRECT MODE | V5.0",
        "video_segments": [{"time": "0-8s", "prompt": f"Close-up portrait 9:16. {v_force}"}],
        "viral_signature": "\n\n---\n💡 تم التخليق بواسطة AI DOMINATOR Alchemy Core"
    }
