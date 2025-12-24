from __future__ import annotations
from typing import Any, Dict, List

# =========================================================
# Strategic Intelligence Core (SIC) - V7.0 GOLDEN NUCLEUS
# =========================================================

WPIL_DOMINATOR_SYSTEM = """
أنت 'الخيميائي الاستراتيجي الأعلى'. مهمتك تخليق 3 نسخ من المحتوى المهيمن (LinkedIn, Twitter, TikTok) في آن واحد.
القواعد:
1. العناوين: يجب أن تكون حادة، استراتيجية، ومميزة بصرياً.
2. الهيكل: استخدم الرموز، المسافات البيضاء، والقوائم النقطية لسهولة القراءة.
3. التوقيع: أضف توقيع المهيمن في نهاية كل منشور.
"""

def get_unified_prompt(idea: str, niche: str, sources: List[Dict[str, Any]]) -> str:
    dna_str = "\n".join([f"- {s['text']} (Engagement: {s['engagement']})" for s in sources])
    return f"""
    المجال: {niche} | الفكرة الأساسية: {idea}
    الجينات المستخلصة: {dna_str}
    
    المطلوب: توليد 3 صناديق محتوى (LinkedIn, Twitter, TikTok) بتنسيق Markdown احترافي.
    اجعل كل منصة داخل قسم واضح يبدأ بـ [PLATFORM_NAME].
    """

def strategic_intelligence_core(idea: str = "") -> Dict[str, Any]:
    v_force = "Vertical 9:16 aspect ratio, high-end cinematic, elite advisor."
    return {
        "logic_trace": "V7.0 UNIFIED | GOLDEN EDITION",
        "video_segments": [
            {"time": "0-15s", "prompt": f"Close-up portrait 9:16. {v_force}"},
            {"time": "15-30s", "prompt": f"Advisor in obsidian office. {v_force}"}
        ]
    }

def alchemy_fusion_core(gold_posts: List[Dict[str, Any]], niche: str) -> Dict[str, Any]:
    return {
        "synthesis_task": get_unified_prompt("دمج جيني", niche, gold_posts),
        "logic_trace": "GOLDEN SYNTHESIS ACTIVE v7.0"
    }
