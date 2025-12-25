from __future__ import annotations
from typing import Any, Dict, List

# =========================================================
# Strategic Intelligence Core (SIC) - V12.0 VISUAL DOMINANCE
# =========================================================

WPIL_DOMINATOR_SYSTEM = """
أنت 'الخيميائي الاستراتيجي الأعلى'. مهمتك تخليق حزم محتوى (LinkedIn, X, TikTok) + تصميم مفهوم بصري فخم.
اللغة: عربية نخبوية. التنسيق: فخامة استراتيجية مطلقة.
الرد: يجب فصل المنصات بـ [LINKEDIN], [TWITTER], [TIKTOK] وإضافة قسم [VISUAL_PROMPT] بالإنجليزية في النهاية.
"""

def strategic_intelligence_core(idea: str = "") -> Dict[str, Any]:
    # أوامر الأبعاد الطولية لـ TikTok
    v_force = "Vertical 9:16, cinematic 8k, mobile framing."
    return {
        "logic_trace": "SIC v12.0 | VISUAL ENGINE ACTIVE",
        "video_segments": [
            {"time": "0-15s", "prompt": f"Close-up of advisor with holographic data eyes. {v_force}"},
            {"time": "15-30s", "prompt": f"Advisor walking in digital obsidian sanctuary. {v_force}"}
        ]
    }

def alchemy_fusion_core(gold_posts: List[Dict[str, Any]], niche: str) -> Dict[str, Any]:
    dna_str = "\n".join([f"- {str(p.get('text'))[:150]}" for p in gold_posts])
    return {
        "synthesis_task": f"تخليق مرسوم سيادي لنيش {niche} بناءً على هذه الجينات:\n{dna_str}\nصمم أيضاً [VISUAL_PROMPT] بالإنجليزية يصف صورة سينمائية فخمة تعبر عن هذا المحتوى.",
        "logic_trace": "ALCHEMY v12.0 | VISUAL SYNTHESIS ENABLED"
    }
