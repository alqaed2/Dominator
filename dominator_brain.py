from __future__ import annotations
from typing import Any, Dict, List

# =========================================================
# Strategic Intelligence Core (SIC) - V4.0 SUPREME
# =========================================================

WPIL_DOMINATOR_SYSTEM = """
أنت 'المستشار الأعلى' (THE SUPREME ADVISOR). 
هويتك: نخبوي، استراتيجي، وصاحب سلطة معرفية مطلقة.
"""

def strategic_intelligence_core(idea: str = "", platform: str = "linkedin", style: str = "default", reference_post: str = "") -> Dict[str, Any]:
    idea_clean = str(idea or "السيادة التقنية").strip()
    ref_clean = str(reference_post or "").strip()
    
    # ميثاق الأبعاد الطولية لـ TikTok
    v_force = "Vertical 9:16 portrait orientation, mobile-first view, high-end studio,"
    char_dna = "ultra-realistic cinematic 8k, elite male advisor, bespoke suit,"
    
    scenes = [
        {"time": "0-8s", "prompt": f"{v_force} Extreme close-up of advisor's face. {char_dna}"},
        {"time": "8-16s", "prompt": f"{v_force} Medium shot of advisor in luxury office. {char_dna}"},
        {"time": "16-24s", "prompt": f"{v_force} Close-up of hands with luxury watch. {char_dna}"},
        {"time": "24-32s", "prompt": f"{v_force} Advisor looking at holographic data. {char_dna}"}
    ]

    return {
        "transformed_input": f"توليد قيادي لـ [{idea_clean}]" if not ref_clean else f"دمج سيادي لـ [{idea_clean}]",
        "logic_trace": f"MODE: VERTICAL 9:16 | STATUS: OPTIMIZED",
        "video_segments": scenes,
        "viral_signature": "\n\n---\n💡 تم تصميم هذه الاستراتيجية بواسطة AI DOMINATOR (SIC v4.0)"
    }
