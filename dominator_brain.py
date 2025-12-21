from __future__ import annotations
from typing import Any, Dict, List

# =========================================================
# Strategic Intelligence Core (SIC) - V4.0 VERTICAL DOMINANCE
# =========================================================

WPIL_DOMINATOR_SYSTEM = """
أنت 'المستشار الأعلى' (THE SUPREME ADVISOR). 
هويتك: نخبوي، استراتيجي، وصاحب سلطة معرفية مطلقة.
"""

def strategic_intelligence_core(idea: str = "", platform: str = "linkedin", style: str = "default", reference_post: str = "") -> Dict[str, Any]:
    idea_clean = str(idea or "الهيمنة الرقمية").strip()
    ref_clean = str(reference_post or "").strip()
    
    # درجة الهيمنة
    dominance_score = 92 
    
    # ميثاق الأبعاد الطولية لـ TikTok (إجبار المحرك البصري)
    # نستخدم كلمات (Vertical, Portrait, 9:16) في البداية والوسط والنهاية
    vertical_force = "Vertical 9:16 portrait orientation, full-body smartphone framing, mobile-first view,"
    character_dna = "ultra-realistic cinematic 8k, elite male advisor in bespoke suit, high-status atmosphere,"
    background_dna = "luxurious minimalist obsidian office, soft cinematic lighting, bokeh background."

    scenes = [
        {"time": "0-8s", "prompt": f"{vertical_force} Extreme close-up of the advisor's face, 9:16 portrait mode. {character_dna} {background_dna} Vertical framing."},
        {"time": "8-16s", "prompt": f"{vertical_force} Medium shot of the advisor walking, 9:16 portrait orientation. {character_dna} {background_dna} Mobile format."},
        {"time": "16-24s", "prompt": f"{vertical_force} Portrait shot, advisor looking at holographic charts, 9:16 aspect ratio. {character_dna} {background_dna} Smartphone layout."},
        {"time": "24-32s", "prompt": f"{vertical_force} Final heroic portrait shot, advisor looking into camera, 9:16 vertical. {character_dna} {background_dna}"}
    ]

    return {
        "transformed_input": f"توليد قيادي للفكرة [{idea_clean}]" if not ref_clean else f"دمج سيادي للفكرة [{idea_clean}]",
        "logic_trace": f"MODE: VERTICAL 9:16 | SCORE: {dominance_score}% | STATUS: OPTIMIZED FOR MOBILE",
        "video_segments": scenes,
        "viral_signature": f"\n\n---\n💡 تم هندسة هذا المحتوى بصرياً بواسطة AI DOMINATOR (v4.0)"
    }
