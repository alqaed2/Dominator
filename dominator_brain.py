from __future__ import annotations
from typing import Any, Dict, List

# =========================================================
# Strategic Intelligence Core (SIC) - V3.0 CINEMATIC SEGMENTS
# =========================================================

WPIL_DOMINATOR_SYSTEM = """
أنت 'المستشار الأعلى' (THE SUPREME ADVISOR). 
هويتك البصرية: بشرية فائقة (High-End Human-Cybernetic Hybrid).
الستايل: هدوء، فخامة، سلطة مطلقة.
"""

def get_segmented_prompts(topic: str) -> List[Dict[str, str]]:
    """
    توليد مشاهد منفصلة، كل مشهد 8 ثوانٍ بتفاصيل سينمائية.
    """
    base_style = "Vertical 9:16 aspect ratio, Ultra-realistic, Cinematic 8k, high-end obsidian office, soft golden lighting."
    character = "Elite male strategic advisor, human skin with subtle glowing cybernetic temple implant, bespoke charcoal suit."

    scenes = [
        {
            "time": "00-08s (The Hook)",
            "prompt": f"Extreme close-up of {character}'s eyes reflecting holographic data. {base_style} Shallow depth of field, sharp focus."
        },
        {
            "time": "08-16s (The Context)",
            "prompt": f"Medium shot of {character} standing in front of a giant transparent glass window overlooking a futuristic automated warehouse. {base_style} Cinematic movement."
        },
        {
            "time": "16-24s (The Action)",
            "prompt": f"Over-the-shoulder shot of {character} swiping a holographic interface. High-speed robotic arms moving in background blur. {base_style}"
        },
        {
            "time": "24-32s (The Authority)",
            "prompt": f"Low angle heroic shot of {character} walking towards the camera. Motion blur, high-status atmosphere, epic lighting. {base_style}"
        }
    ]
    return scenes

def strategic_intelligence_core(idea: str = "", platform: str = "linkedin", style: str = "default", reference_post: str = "") -> Dict[str, Any]:
    idea_clean = str(idea or "الهيمنة السوقية").strip()
    ref_clean = str(reference_post or "").strip()
    
    # تحديد المهمة
    task = f"توليد محتوى قيادي للفكرة: [{idea_clean}]"
    if ref_clean:
        task = f"دمج استراتيجي بين الفكرة [{idea_clean}] والمنشور [{ref_clean}]"

    result = {
        "transformed_input": task,
        "logic_trace": f"MODE: CINEMATIC SEGMENTS | PLATFORM: {platform.upper()}",
    }

    if platform == "tiktok":
        result["video_segments"] = get_segmented_prompts(idea_clean)

    return result
