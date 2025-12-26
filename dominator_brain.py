from __future__ import annotations
from typing import Any, Dict, List

# =========================================================
# Strategic Intelligence Core (SIC) - V12.8 FINAL STABILITY
# =========================================================

WPIL_DOMINATOR_SYSTEM = """
أنت 'الخيميائي الاستراتيجي الأعلى'. مهمتك تخليق حزم محتوى سيادية (LinkedIn, X, TikTok).
القواعد: لغة نخبوية استراتيجية، عناوين حادة، وتقسيم احترافي.
يجب فصل المنصات بـ [LINKEDIN], [TWITTER], [TIKTOK] وإضافة [VISUAL_PROMPT] في النهاية.
"""

def strategic_intelligence_core(idea: str = "") -> Dict[str, Any]:
    v_force = "Vertical 9:16 aspect ratio, high-end professional cinematic studio, 8k portrait."
    return {
        "logic_trace": "SIC v12.8 | STABILITY LOCKDOWN",
        "video_segments": [
            {"time": "0-15s", "prompt": f"Professional close-up of advisor with intense gaze 9:16. {v_force}"},
            {"time": "15-30s", "prompt": f"Advisor in a minimalist luxury boardroom office 9:16. {v_force}"}
        ]
    }

def alchemy_fusion_core(gold_posts: List[Dict[str, Any]], niche: str) -> Dict[str, Any]:
    dna = [f"Text: {p['text']} | Stats: {p.get('engagement', 'High')}" for p in gold_posts]
    return {
        "synthesis_task": f"تخليق مرسوم سيادي لنيش {niche} بناءً على الجينات التالية:\n{dna}\nصمم [VISUAL_PROMPT] بالإنجليزية لصورة فوتوغرافية واقعية للأعمال.",
        "logic_trace": "SYNTHESIS ACTIVE v12.8"
    }
