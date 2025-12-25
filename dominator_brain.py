from __future__ import annotations
from typing import Any, Dict, List

# =========================================================
# Strategic Intelligence Core (SIC) - V11.0 COMMAND & CONTROL
# =========================================================

WPIL_DOMINATOR_SYSTEM = """
أنت 'الخيميائي الاستراتيجي الأعلى'. مهمتك تخليق حزم محتوى سيادية لـ (LinkedIn, X, TikTok).
اللغة: عربية نخبوية حادة. التنسيق: فخامة استراتيجية.
يجب فصل المنصات بـ [LINKEDIN], [TWITTER], [TIKTOK].
"""

def strategic_intelligence_core(idea: str = "") -> Dict[str, Any]:
    v_force = "Vertical 9:16 aspect ratio, cinematic 8k, advisor character."
    return {
        "logic_trace": "SIC v11.0 | DUAL-MODE ENABLED",
        "video_segments": [
            {"time": "0-15s", "prompt": f"Extreme close-up of advisor with holographic eyes 9:16. {v_force}"},
            {"time": "15-30s", "prompt": f"Advisor walking in digital obsidian vault 9:16. {v_force}"}
        ]
    }

def alchemy_fusion_core(gold_posts: List[Dict[str, Any]], niche: str) -> Dict[str, Any]:
    dna_str = "\n".join([f"- {str(p.get('text'))[:150]}" for p in gold_posts])
    return {
        "synthesis_task": f"تخليق مرسوم خارق لنيش {niche} بناءً على هذه الجينات المستهدفة:\n{dna_str}",
        "logic_trace": "ALCHEMY FUSION v11.0 ACTIVE"
    }
