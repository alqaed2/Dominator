from __future__ import annotations
from typing import Any, Dict, List

# =========================================================
# Strategic Intelligence Core (SIC) - V10.8 STEALTH HUNTER
# =========================================================

WPIL_DOMINATOR_SYSTEM = """
أنت 'الخيميائي الاستراتيجي الأعلى'. مهمتك تخليق محتوى مهيمن لـ (LinkedIn, X, TikTok).
القواعد: لغة نخبوية استراتيجية، عناوين حادة، تقسيم احترافي بـ [LINKEDIN], [TWITTER], [TIKTOK].
"""

def strategic_intelligence_core(idea: str = "") -> Dict[str, Any]:
    v_force = "Vertical 9:16 aspect ratio, cinematic 8k, advisor character."
    return {
        "logic_trace": "SIC v10.8 | STEALTH HUNTER ACTIVE",
        "video_segments": [
            {"time": "0-15s", "prompt": f"Close-up of advisor with holographic data eyes 9:16. {v_force}"},
            {"time": "15-30s", "prompt": f"Advisor walking in digital obsidian sanctuary 9:16. {v_force}"}
        ]
    }

def alchemy_fusion_core(gold_posts: List[Dict[str, Any]], niche: str) -> Dict[str, Any]:
    dna_str = "\n".join([f"- {str(p.get('text'))[:150]}" for p in gold_posts])
    return {
        "synthesis_task": f"تخليق مرسوم خارق لنيش {niche} بناءً على هذه الجينات:\n{dna_str}",
        "logic_trace": "NEBULA SYNTHESIS v10.8 ACTIVE"
    }
