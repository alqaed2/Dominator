from __future__ import annotations
from typing import Any, Dict, List

# =========================================================
# Strategic Intelligence Core (SIC) - V5.1 ALCHEMY & VERTICAL
# =========================================================

WPIL_DOMINATOR_SYSTEM = """
أنت 'الخيميائي الاستراتيجي الأعلى' (THE SUPREME ALCHEMIST). 
مهمتك: تشريح المحتوى العالمي الناجح، استخلاص الجينات الفيروسية، وتخليق منشورات خارقة تمتلك سلطة معرفية مطلقة.
اللغة: العربية النخبوية.
"""

def alchemy_fusion_core(gold_posts: List[Dict[str, Any]], niche: str) -> Dict[str, Any]:
    """مفاعل الاندماج: تحويل المواد الخام إلى ذهب استراتيجي."""
    dna_samples = [f"Post: {p['text']} | Stats: {p['engagement']}" for p in gold_posts]
    
    synthesis_task = f"""
    المجال: {niche}
    العينات الذهبية (DNA Samples):
    {dna_samples}
    
    المطلوب:
    1. استخلص 'الخطاف' (Hook) الذي لا يمكن مقاومته.
    2. صمم 'الهيكل' (Structure) بناءً على أكثر العينات تفاعلاً.
    3. ادمج 'السلطة المعرفية' في صياغة المحتوى.
    4. أنتج منشوراً واحداً خارقاً يتفوق على هذه العينات.
    """
    
    return {
        "synthesis_task": synthesis_task,
        "dominance_score": 98,
        "logic_trace": f"SYNTHESIS ACTIVE | FUSED {len(gold_posts)} SAMPLES | NICHE: {niche}"
    }

def strategic_intelligence_core(idea: str = "", platform: str = "linkedin", style: str = "default", reference_post: str = "") -> Dict[str, Any]:
    """المحرك الاستراتيجي للنتائج الفردية والطولية."""
    idea_clean = str(idea or "السيادة الرقمية").strip()
    ref_clean = str(reference_post or "").strip()
    
    # ميثاق الأبعاد الطولية 9:16 لـ TikTok
    v_force = "Vertical 9:16 aspect ratio, portrait orientation, high-end mobile framing,"
    char_dna = "ultra-realistic cinematic 8k, elite male advisor in bespoke suit,"
    
    scenes = [
        {"time": "0-8s", "prompt": f"{v_force} Extreme close-up of advisor's eyes. {char_dna}"},
        {"time": "8-16s", "prompt": f"{v_force} Medium shot of advisor in high-tech office. {char_dna}"},
        {"time": "16-24s", "prompt": f"{v_force} Close-up of hands manipulating holographic charts. {char_dna}"},
        {"time": "24-32s", "prompt": f"{v_force} Heroic low-angle shot of advisor looking at camera. {char_dna}"}
    ]

    return {
        "transformed_input": f"توليد قيادي لـ [{idea_clean}]" if not ref_clean else f"دمج سيادي لـ [{idea_clean}]",
        "logic_trace": f"MODE: VERTICAL 9:16 | PLATFORM: {platform.upper()}",
        "video_segments": scenes,
        "viral_signature": "\n\n---\n💡 تم الهندسة بواسطة AI DOMINATOR Alchemy Core"
    }
