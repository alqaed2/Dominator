from __future__ import annotations
from typing import Any, Dict, List

# =========================================================
# Strategic Intelligence Core (SIC) - V8.5 NEBULA NUCLEUS
# =========================================================

WPIL_DOMINATOR_SYSTEM = """
أنت 'الخيميائي الاستراتيجي الأعلى'. مهمتك تخليق محتوى مهيمن لـ (LinkedIn, X, TikTok).
القواعد الصارمة:
1. التنسيق: استخدم لغة نخبوية، عناوين حادة، ومسافات واسعة.
2. الرد الموحد: يجب أن يحتوي ردك على المنصات الثلاث مفصولة بالعلامات التالية:
   [LINKEDIN] لنسخة لينكد إن.
   [TWITTER] لنسخة إكس (ثريد).
   [TIKTOK] لسكريبت تيك توك.
"""

def strategic_intelligence_core(idea: str = "") -> Dict[str, Any]:
    v_force = "Vertical 9:16 portrait, cinematic 8k, elite advisor character."
    return {
        "logic_trace": "NEBULA v8.5 | FAILOVER ENABLED",
        "video_segments": [
            {"time": "0-15s", "prompt": f"Close-up of advisor with holographic eyes 9:16. {v_force}"},
            {"time": "15-30s", "prompt": f"Full body shot walking in obsidian lab 9:16. {v_force}"}
        ]
    }

def alchemy_fusion_core(gold_posts: List[Dict[str, Any]], niche: str) -> Dict[str, Any]:
    dna_str = "\n".join([f"- {str(p.get('text'))[:150]}" for p in gold_posts])
    return {
        "synthesis_task": f"تخليق مرسوم خارق لنيش {niche} باستخدام هذه الجينات الحية:\n{dna_str}\nيجب تقسيم المخرجات بـ [LINKEDIN], [TWITTER], [TIKTOK].",
        "logic_trace": "NEBULA ALCHEMY v8.5 ACTIVE"
    }
