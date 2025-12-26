from __future__ import annotations
from typing import Any, Dict, List

# =========================================================
# Strategic Intelligence Core (SIC) - V13.0 CINEMATIC
# =========================================================

WPIL_DOMINATOR_SYSTEM = """
أنت 'الخيميائي الاستراتيجي الأعلى'. مهمتك تخليق حزم محتوى سيادية (نص + صورة + مخطط فيديو سينمائي).
اللغة: عربية نخبوية حادة. التنسيق: فخامة استراتيجية.
يجب فصل المنصات بـ [LINKEDIN], [TWITTER], [TIKTOK] وإضافة [VISUAL_PROMPT] في النهاية.
"""

def strategic_intelligence_core(idea: str = "") -> Dict[str, Any]:
    # أوامر قهرية للفيديو السينمائي الفخم 9:16
    v_force = "Vertical 9:16 portrait, ultra-realistic 8k cinematic, high-end studio lighting."
    advisor_dna = "Elite strategic advisor, sharp features, tailored charcoal suit, authoritative presence."

    scenes = [
        {
            "time": "0-10s (The Hook)",
            "prompt": f"{v_force} Close-up of {advisor_dna} eyes reflecting holographic data. Sharp focus."
        },
        {
            "time": "10-20s (The Logic)",
            "prompt": f"{v_force} Medium shot of {advisor_dna} standing by a luxury boardroom window overlooking a futuristic Riyadh skyline."
        },
        {
            "time": "20-30s (The Command)",
            "prompt": f"{v_force} Macro shot of advisor's hand signing a digital glass tablet with a glowing gold stylus."
        }
    ]
    return {
        "logic_trace": "SIC v13.0 | CINEMATIC BLUEPRINT ACTIVE",
        "video_segments": scenes
    }

def alchemy_fusion_core(gold_posts: List[Dict[str, Any]], niche: str) -> Dict[str, Any]:
    dna = [f"Post: {p['text']} | Stats: {p.get('engagement', 'High')}" for p in gold_posts]
    return {
        "synthesis_task": f"تخليق مرسوم سيادي لنيش {niche} بناءً على الجينات التالية:\n{dna}\nصمم [VISUAL_PROMPT] بالإنجليزية لصورة فوتوغرافية واقعية للأعمال.",
        "logic_trace": "SYNTHESIS ACTIVE v13.0"
    }
